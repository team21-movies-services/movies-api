from http import HTTPStatus
from typing import Any
from unittest import TestCase

import pytest
from redis.asyncio import Redis

from src.api.errors import APIErrorDetail
from tests.functional.testdata.films import get_film_list
from tests.functional.utils.elastic.indices import EsIndices
from tests.functional.utils.fixture_types import EsDeleteData, EsWriteData, MakeHTTPGetRequest

INDEX_NAME = EsIndices.MOVIES.value[0]
SEARCH_URL = "films/search"


@pytest.fixture
async def es_data(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
):
    films = get_film_list()
    await es_write_data(films, INDEX_NAME)

    yield films

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_search(
    es_data,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование films/search"""
    response = await make_get_request(SEARCH_URL)

    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == len(es_data)


@pytest.mark.asyncio
async def test_films_search_pagination_page_size(
    es_data,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование размера пагинации."""

    page_size = 2

    response = await make_get_request(SEARCH_URL, {"page_size": page_size})

    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == page_size
    assert response.body["pages"] == len(es_data) / page_size


@pytest.mark.asyncio
async def test_films_search_pagination_next_page(
    es_data,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование запроса следующей страницы."""

    page_size = 2

    response = await make_get_request(SEARCH_URL, {"page": 2, "page_size": page_size})

    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == page_size


@pytest.mark.asyncio
async def test_films_search_search_after(
    es_data,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование пагинации с использованием search_after."""

    page_size = 2

    first_response = await make_get_request(SEARCH_URL, {"page_size": page_size})

    search_after = ",".join(map(str, first_response.body["search_after"]))
    second_response = await make_get_request(SEARCH_URL, {"page_size": page_size, "search_after": search_after})

    assert first_response.status == HTTPStatus.OK
    assert second_response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_films_search_search_after_pagination(
    es_data,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование запроса следующей страницы с помощью search_after."""

    first_part_page_size = 4
    response = await make_get_request(SEARCH_URL, {"page_size": first_part_page_size})
    first_part_items = response.body["items"]

    second_part_page_size = 2
    second_part_items = []

    response = await make_get_request(SEARCH_URL, {"page_size": second_part_page_size})
    second_part_items += response.body["items"]

    search_after = ",".join(map(str, response.body["search_after"]))
    response = await make_get_request(SEARCH_URL, {"page_size": second_part_page_size, "search_after": search_after})
    second_part_items += response.body["items"]

    TestCase().assertCountEqual(first_part_items, second_part_items)


@pytest.mark.parametrize(
    "query, expected_film_title",
    [
        ("Wookiees", "Star Wars Galaxies: Rage of the Wookiees"),
        ("Blips", "Star Wars Blips"),
    ],
)
@pytest.mark.asyncio
async def test_films_search_query(
    es_data,
    make_get_request: MakeHTTPGetRequest,
    query: str,
    expected_film_title: str,
):
    """Тестирование поиска по названию."""

    response = await make_get_request(SEARCH_URL, {"query": query})

    assert response.status == HTTPStatus.OK
    assert response.body["items"][0]["title"] == expected_film_title


@pytest.mark.parametrize(
    "query_params",
    [
        {"page_number": "asdads"},
        {"page_number": -1},
        {"page_size": "asdads"},
        {"page_size": -1},
    ],
)
@pytest.mark.asyncio
async def test_films_search_incorrect_queries(
    es_data,
    make_get_request: MakeHTTPGetRequest,
    query_params: dict[str, Any],
):
    """Тестирование граничных случаев по валидации данных."""

    response = await make_get_request(SEARCH_URL, query_params)
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_films_search_incorrect_search_after_param(
    es_data,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование граничных случаев по валидации данных параметра search_after"""

    response = await make_get_request(SEARCH_URL, {"search_after": 12344})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body["detail"] == APIErrorDetail.ELASTIC_SEARCH_AFTER


@pytest.mark.asyncio
async def test_films_search_cache(
    es_data,
    make_get_request: MakeHTTPGetRequest,
    redis_client: Redis,
):
    """Проверка работы кэша."""

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 0

    await make_get_request(SEARCH_URL)

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 1
