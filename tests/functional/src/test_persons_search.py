from http import HTTPStatus
from typing import Any
from unittest import TestCase

import pytest
from redis.asyncio import Redis

from src.api.errors import APIErrorDetail
from tests.functional.testdata.persons import get_persons_list
from tests.functional.utils.elastic.indices import EsIndices
from tests.functional.utils.fixture_types import EsDeleteData, EsWriteData, MakeHTTPGetRequest

INDEX_NAME = EsIndices.PERSONS.value[0]
SEARCH_URL = "persons/search"


@pytest.mark.asyncio
async def test_search_persons(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование persons/search"""

    persons = get_persons_list()
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL)

    assert response.status == HTTPStatus.OK
    TestCase().assertCountEqual(response.body["items"], persons)

    await es_delete_data(INDEX_NAME)


@pytest.mark.parametrize(
    "query_params",
    [
        {"sort": "full_name"},
        {"sort": "-full_name"},
        {"sort": "non_existent"},
    ],
)
@pytest.mark.asyncio
async def test_search_sorting(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    query_params: dict[str, Any],
):
    """Тестирование сортировки личностей."""

    persons = get_persons_list()
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL, query_params)

    assert response.status == HTTPStatus.OK

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_persons_search_pagination(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование размера и количества страниц в пагинации."""

    persons = get_persons_list()
    page_size = 2
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL, {"page_size": page_size})

    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == page_size
    assert response.body["pages"] == len(persons) / page_size

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_persons_search_pagination_next_page(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование запроса следующей страницы."""

    persons = get_persons_list()
    page_size = 2
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL, {"page": page_size, "page_size": page_size})

    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == page_size

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_persons_search_search_after_pagination(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование пагинации с использованием search_after."""

    persons = get_persons_list()
    page_size = 2
    sort_field = "full_name"
    await es_write_data(persons, INDEX_NAME)

    first_response = await make_get_request(SEARCH_URL, {"sort": sort_field, "page_size": page_size})
    search_after = ",".join(map(str, first_response.body["search_after"]))
    second_response = await make_get_request(
        SEARCH_URL, {"sort": sort_field, "page_size": page_size, "search_after": search_after}
    )

    assert first_response.status == HTTPStatus.OK
    assert second_response.status == HTTPStatus.OK

    await es_delete_data(INDEX_NAME)


@pytest.mark.parametrize(
    "query, expected_full_name",
    [
        ("Ross", "Ross Hagen"),
        ("Fred", "Fred Olen Ray"),
    ],
)
@pytest.mark.asyncio
async def test_persons_search_query(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    query: str,
    expected_full_name: str,
):
    """Тестирование поиска по имени."""

    persons = get_persons_list()
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL, {"query": query})

    assert response.status == HTTPStatus.OK
    assert response.body["items"][0]["full_name"] == expected_full_name

    await es_delete_data(INDEX_NAME)


@pytest.mark.parametrize(
    "query_params, expected_http_status",
    [
        ({"page_number": "asdads"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"page_number": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"page_size": "asdads"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"page_size": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ({"sort": "asdads"}, HTTPStatus.OK),
        ({"sort": -1}, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
async def test_persons_search_incorrect_queries(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    query_params: dict[str, Any],
    expected_http_status: int,
):
    """Тестирование граничных случаев по валидации данных."""

    persons = get_persons_list()
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL, query_params)

    assert response.status == expected_http_status

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_persons_search_incorrect_search_after_queries(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование граничных случаев по валидации данных запроса с search_after."""

    persons = get_persons_list()
    await es_write_data(persons, INDEX_NAME)

    response = await make_get_request(SEARCH_URL, {"search_after": 12344, "sort": "full_name"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body["detail"] == APIErrorDetail.ELASTIC_SEARCH_AFTER

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_persons_search_cache(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    redis_client: Redis,
):
    """Проверка работы кэша."""

    persons = get_persons_list()
    await es_write_data(persons, INDEX_NAME)

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 0

    await make_get_request(SEARCH_URL)
    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 1

    await es_delete_data(INDEX_NAME)
