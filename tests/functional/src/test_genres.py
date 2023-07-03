from http import HTTPStatus

import pytest


@pytest.fixture
def es_data():
    return [{"uuid": "109463de-6ddb-4013-8236-338787210dae", "name": "Comedy", "description": "test desc"}]


@pytest.mark.parametrize(
    "uuid_genre",
    [123, 12345, "abcde"],
)
@pytest.mark.asyncio
async def test_get_genre_by_invalid_uuid(
    es_write_data,
    make_get_request,
    es_data,
    uuid_genre,
):
    """Проверка валидации uuid."""
    await es_write_data(es_data, "genres")

    response = await make_get_request(f"genres/{uuid_genre}")

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "uuid_genre, expected_answer",
    [
        (
            "109463de-6ddb-4013-8236-338787210dae",
            {"uuid": "109463de-6ddb-4013-8236-338787210dae", "name": "Comedy"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_genre_by_uuid(
    es_write_data,
    make_get_request,
    es_data,
    uuid_genre,
    expected_answer,
):
    """Поиск конкретного жанра по uuid."""
    await es_write_data(es_data, "genres")

    response = await make_get_request(f"genres/{uuid_genre}")

    assert response.body == expected_answer
    assert response.status == HTTPStatus.OK


@pytest.mark.parametrize(
    "expected_answer",
    [
        [{"uuid": "109463de-6ddb-4013-8236-338787210dae", "name": "Comedy"}],
    ],
)
@pytest.mark.asyncio
async def test_get_list_genres(
    es_write_data,
    make_get_request,
    es_data,
    expected_answer,
):
    """Вывести все жанры."""
    await es_write_data(es_data, "genres")

    response = await make_get_request("genres")

    assert len(response.body) == 1
    assert response.body == expected_answer
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_genre_cache(
    redis_client,
    es_write_data,
    make_get_request,
    es_data,
):
    """Проверка работы кэша."""
    await es_write_data(es_data, "genres")

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 0

    response = await make_get_request("genres")
    keys = await redis_client.keys(pattern="*")

    assert len(keys) == 1
    assert len(response.body) == 1
    assert response.status == HTTPStatus.OK
