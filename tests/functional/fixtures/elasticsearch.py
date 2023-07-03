import json

import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError

from tests.functional.settings import test_settings
from tests.functional.utils.elastic.indices import EsIndices


@pytest.fixture
async def es_client():
    es_client = AsyncElasticsearch(hosts=[f"{test_settings.elastic_host}:{test_settings.elastic_port}"])
    yield es_client
    await es_client.close()


def get_es_bulk_query(es_data, es_index, es_id_field):
    bulk_query = []
    for row in es_data:
        bulk_query.extend([json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}), json.dumps(row)])
    return "\n".join(bulk_query) + "\n"


@pytest.fixture
async def es_create_indices(es_client: AsyncElasticsearch) -> None:
    """Создаёт индексы если они не существуют"""
    for index in EsIndices:
        index_name, index_declaration = index.value
        try:
            await es_client.indices.get(index_name)
        except NotFoundError:
            await es_client.indices.create(index_name, index_declaration)


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch, es_create_indices):
    async def inner(data: list[dict], es_index: str) -> None:
        bulk_query = get_es_bulk_query(data, es_index, test_settings.es_id_field)
        response = await es_client.bulk(bulk_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def es_delete_data(es_client: AsyncElasticsearch):
    async def inner(es_index: str) -> None:
        await es_client.indices.delete(es_index)

    return inner
