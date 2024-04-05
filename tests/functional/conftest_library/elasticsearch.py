from typing import Any, Mapping

import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import settings, es_settings


@pytest_asyncio.fixture(scope="session")
async def es():
    host = settings.elastic_host
    port = settings.elastic_port

    es = AsyncElasticsearch(hosts=f'http://{host}:{port}', verify_certs=False, request_timeout=3)
    yield es
    await es.close()


@pytest_asyncio.fixture(scope="session")
async def es_write_data(es: AsyncElasticsearch):
    async def inner(data: list[dict[str, Any]], index: str, mappings: Mapping, settings: Mapping):
        if await es.indices.exists(index=index):
            await es.indices.delete(index=index)
        await es.indices.create(index=index, mappings=mappings, settings=settings)

        updated, errors = await async_bulk(client=es, actions=data, refresh=True)

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(scope='session')
async def upload_data_to_es(
        es_write_data,
        film_data,
        person_data
):
    await es_write_data(
        film_data,
        es_settings.movies_index_name,
        es_settings.movies_mappings,
        es_settings.movies_settings
    )

    await es_write_data(
        person_data,
        es_settings.persons_index_name,
        es_settings.persons_mappings,
        es_settings.persons_settings
    )


@pytest_asyncio.fixture(scope="session")
async def es_delete_data(es):
    async def inner(id: str, index: str):
        await es.delete(id=id, index=index)

    return inner
