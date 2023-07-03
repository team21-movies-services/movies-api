from http import HTTPStatus
from typing import Any
from unittest import TestCase

import pytest
from redis.asyncio import Redis

from src.api.errors import APIErrorDetail
from tests.functional.testdata.films import films_length, get_film, get_film_list, not_existing_film_uuid
from tests.functional.testdata.genres import not_existing_genre_uuid
from tests.functional.utils.elastic.indices import EsIndices
from tests.functional.utils.fixture_types import EsDeleteData, EsWriteData, MakeHTTPGetRequest

INDEX_NAME = EsIndices.MOVIES.value[0]


@pytest.mark.asyncio
async def test_get_film_by_uuid(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Поиск фильма по uuid."""

    film = get_film()
    await es_write_data([film], INDEX_NAME)

    response = await make_get_request(f"films/{film['uuid']}")

    assert response.body == film
    assert response.status == HTTPStatus.OK

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_can_not_get_film_by_not_existing_uuid(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Поиск фильма по несуществующему uuid."""

    film = get_film()
    await es_write_data([film], INDEX_NAME)

    response = await make_get_request(f"films/{not_existing_film_uuid}")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == APIErrorDetail.FILM_NOT_FOUND

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_get_all_films(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Поиск всех фильмов."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    response = await make_get_request("films/")

    assert response.status == HTTPStatus.OK
    assert len(response.body["items"]) == films_length

    expected_answer = [
        {"uuid": film["uuid"], "title": film["title"], "imdb_rating": film["imdb_rating"]} for film in film_list
    ]

    TestCase().assertCountEqual(response.body["items"], expected_answer)
    assert response.body["pages"] == 1

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_sorting(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование сортировки фильмов."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    response = await make_get_request("films/", {"sort": "imdb_rating"})

    assert response.status == HTTPStatus.OK

    expected_answer = sorted(
        [{"uuid": film["uuid"], "title": film["title"], "imdb_rating": film["imdb_rating"]} for film in film_list],
        key=lambda item: item["imdb_rating"],
    )
    assert response.body["items"] == expected_answer

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def films_sorting_non_existent_sorting_field(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование сортировки фильмов по несуществующему полю."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    response = await make_get_request("films/", {"sort": "not_exists"})
    assert response.status == HTTPStatus.OK

    expected_answer = [
        {"uuid": film["uuid"], "title": film["title"], "imdb_rating": film["imdb_rating"]} for film in film_list
    ]
    TestCase().assertCountEqual(response.body["items"], expected_answer)

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_pagination(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование пагинации."""

    film_list = get_film_list()
    page_size = 2
    await es_write_data(film_list, INDEX_NAME)

    # test page size
    response = await make_get_request("films/", {"page_size": page_size})
    assert response.status == HTTPStatus.OK

    assert len(response.body["items"]) == page_size
    assert response.body["pages"] == films_length / page_size

    # test search after
    response = await make_get_request("films/", {"sort": "imdb_rating", "page_size": page_size})
    assert response.status == HTTPStatus.OK

    expected_answer = sorted(
        [{"uuid": film["uuid"], "title": film["title"], "imdb_rating": film["imdb_rating"]} for film in film_list],
        key=lambda item: item["imdb_rating"],
    )

    expected_search_after = [expected_answer[1]["imdb_rating"], expected_answer[1]["uuid"]]
    assert response.body["search_after"] == expected_search_after
    assert response.body["items"] == expected_answer[0:2]

    search_after = ",".join(map(str, response.body["search_after"]))
    response = await make_get_request(
        "films/", {"sort": "imdb_rating", "page_size": page_size, "search_after": search_after}
    )
    assert response.status == HTTPStatus.OK

    expected_search_after = [expected_answer[3]["imdb_rating"], expected_answer[3]["uuid"]]
    assert response.body["search_after"] == expected_search_after
    assert response.body["items"] == expected_answer[2:4]

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_genre_query(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Поиск фильмов по жанру."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    genres = {}
    for film in film_list:
        for genre in film["genre"]:
            genre_uuid = genre["uuid"]
            if genre_uuid not in genres:
                genres[genre_uuid] = 0
            genres[genre_uuid] += 1

    for genre_uuid in genres:
        response = await make_get_request("films/", {"genre": genre_uuid})

        assert response.status == HTTPStatus.OK
        assert len(response.body["items"]) == genres[genre_uuid]

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_non_existent_genre_query(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Поиск фильмов по несуществующему жанру."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    response = await make_get_request("films/", {"genre": not_existing_genre_uuid})

    assert response.status == HTTPStatus.OK
    assert response.body["items"] == []
    assert response.body["pages"] == 0

    await es_delete_data(INDEX_NAME)


@pytest.mark.parametrize(
    "path, query_params, expected_http_status",
    [
        ("films/123", None, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"page_number": "asdads"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"page_number": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"page_size": "asdads"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"page_size": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"sort": "asdads"}, HTTPStatus.OK),
        ("films/", {"sort": -1}, HTTPStatus.OK),
        ("films/", {"genre": "asdads"}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"genre": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"page_size": -1}, HTTPStatus.UNPROCESSABLE_ENTITY),
        ("films/", {"sort": "asdads"}, HTTPStatus.OK),
        ("films/", {"sort": -1}, HTTPStatus.OK),
    ],
)
@pytest.mark.asyncio
async def test_films_incorrect_queries(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    path: str,
    query_params: dict[str, Any],
    expected_http_status: int,
):
    """Тестирование граничных случаев по валидации данных."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    response = await make_get_request(path, query_params)

    assert response.status == expected_http_status

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_incorrect_queries_search_after(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
):
    """Тестирование граничных случаев по валидации данных с использоваинем search_after."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    response = await make_get_request("films/", {"search_after": 12344, "sort": "imdb_rating"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body["detail"] == APIErrorDetail.ELASTIC_SEARCH_AFTER

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_films_cache(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    redis_client: Redis,
):
    """Проверка работы кэша films."""

    film_list = get_film_list()
    await es_write_data(film_list, INDEX_NAME)

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 0

    await make_get_request("films/")
    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 1

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_film_cache(
    es_write_data: EsWriteData,
    es_delete_data: EsDeleteData,
    make_get_request: MakeHTTPGetRequest,
    redis_client: Redis,
):
    """Проверка работы кэша film/uuid."""

    film = get_film()
    await es_write_data([film], INDEX_NAME)

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 0

    await make_get_request(f"films/{film['uuid']}")
    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 1

    await es_delete_data(INDEX_NAME)
