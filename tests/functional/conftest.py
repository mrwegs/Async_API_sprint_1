import asyncio
import uuid
from typing import Mapping

import aiohttp
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from redis.asyncio import Redis

from tests.functional.settings import dev_settings as settings, es_settings


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def redis():
    redis = Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    yield redis
    await redis.close()


@pytest_asyncio.fixture(scope="session")
async def es():
    host = settings.elastic_host
    port = settings.elastic_port

    es = AsyncElasticsearch(hosts=f'http://{host}:{port}', verify_certs=False)
    yield es
    await es.close()


@pytest_asyncio.fixture(scope="session")
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def make_get_request(client_session: aiohttp.ClientSession):
    async def inner(uri: str, data: Mapping = None):
        url = settings.service_url + uri

        async with client_session.get(url, params=data) as response:
            body = await response.json()
            status = response.status

            return body, status

    return inner


@pytest_asyncio.fixture(scope="session")
async def es_write_data(es: AsyncElasticsearch):
    async def inner(data: list[Mapping], index: str, mappings: Mapping, settings: Mapping):
        if await es.indices.exists(index=index):
            await es.indices.delete(index=index)
        await es.indices.create(index=index, mappings=mappings, settings=settings)

        updated, errors = await async_bulk(client=es, actions=data, refresh="wait_for")

        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest_asyncio.fixture(scope="session")
async def es_delete_data(es):
    async def inner(id: str, index: str):
        await es.delete(id=id, index=index)

    return inner


@pytest_asyncio.fixture(scope="session")
def film_data():
    es_data = [{
        'uuid': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'uuid': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
            {'uuid': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
        ],
        'writers': [
            {'uuid': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
            {'uuid': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
        ],
    } for _ in range(60)]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': 'movies', '_id': row['uuid']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope="session")
def person_data():
    index_name = es_settings.persons_index_name
    es_data = [{
        'uuid': str(uuid.uuid4()),
        'full_name': 'Anna De Armas',
        'films': [
            {'uuid': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'title': 'Blade Runner', 'imdb_rating': 8.0,
             'roles': ['actor']},
            {'uuid': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'title': 'Knives Out', 'imdb_rating': 7.9,
             'roles': ['actor']},
        ],
    } for _ in range(60)]

    bulk_query: list[dict] = []
    for row in es_data:
        data = {'_index': index_name, '_id': row['uuid']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope="session")
def persons_index_settings():
    index = es_settings.persons_index_name
    mappings = es_settings.persons_mappings
    settings = es_settings.persons_settings

    return index, mappings, settings


@pytest_asyncio.fixture(scope="session")
def movies_index_settings():
    index = es_settings.movies_index_name
    mappings = es_settings.movies_mappings
    settings = es_settings.movies_settings

    return index, mappings, settings


@pytest_asyncio.fixture(scope="session")
def genres_index_settings():
    index = es_settings.genres_index_name
    mappings = es_settings.genres_mappings
    settings = es_settings.genres_settings

    return index, mappings, settings
