from http import HTTPStatus

import pytest

from tests.functional.utils.elastic.indices import EsIndices

INDEX_NAME = EsIndices.PERSONS.value[0]


@pytest.fixture
def es_data():
    return [{"uuid": "f0563be9-c196-4968-9fa3-0ad0d78be63e", "full_name": "Chack Noris"}]


@pytest.mark.parametrize(
    "uuid_person",
    [123, 12345, "abcde"],
)
@pytest.mark.asyncio
async def test_get_person_by_invalid_uuid(
    es_write_data,
    es_delete_data,
    make_get_request,
    es_data,
    uuid_person,
):
    """Проверка валидации uuid."""
    await es_write_data(es_data, INDEX_NAME)

    response = await make_get_request(f"persons/{uuid_person}")

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY

    await es_delete_data(INDEX_NAME)


@pytest.mark.parametrize(
    "uuid_person, expected_answer",
    [
        (
            "f0563be9-c196-4968-9fa3-0ad0d78be63e",
            {"uuid": "f0563be9-c196-4968-9fa3-0ad0d78be63e", "full_name": "Chack Noris", "films": []},
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_person_by_uuid(
    es_write_data,
    es_delete_data,
    make_get_request,
    es_data,
    uuid_person,
    expected_answer,
):
    """Поиск конкретной персону по uuid."""
    await es_write_data(es_data, INDEX_NAME)

    response = await make_get_request(f"persons/{uuid_person}")

    assert response.body == expected_answer
    assert response.status == HTTPStatus.OK

    await es_delete_data(INDEX_NAME)


@pytest.mark.asyncio
async def test_person_cache(
    redis_client,
    es_write_data,
    es_delete_data,
    make_get_request,
    es_data,
):
    """Проверка работы кэша."""
    await es_write_data(es_data, INDEX_NAME)

    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 0

    uuid_person = es_data[0]["uuid"]
    await make_get_request(f"persons/{uuid_person}")
    keys = await redis_client.keys(pattern="*")
    assert len(keys) == 1

    await es_delete_data(INDEX_NAME)
