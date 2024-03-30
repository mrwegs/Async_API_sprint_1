import asyncio

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    host = test_settings.elastic_host
    port = test_settings.elastic_port
    es_client = AsyncElasticsearch(hosts=f'http://{host}:{port}', verify_certs=False)
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='client_session')
async def aiohttp_client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client):
    async def inner(data: list[dict], index: str, mapping: dict):
        if await es_client.indices.exists(index=index):
            await es_client.indices.delete(index=index)
        await es_client.indices.create(index=index, body=mapping)

        updated, errors = await async_bulk(client=es_client, actions=data, refresh='wait_for')

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner
