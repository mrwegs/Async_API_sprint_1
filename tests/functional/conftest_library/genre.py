import uuid
from typing import Any

import pytest_asyncio

from tests.functional.settings import es_settings, settings


@pytest_asyncio.fixture(scope='session')
async def genre_data():
    index_name: str = es_settings.genres_index_name

    es_data = [
        {
            'uuid': str(uuid.uuid4()),
            'name': 'Drama'
        }
        for _ in range(60)]

    bulk_query: list[dict] = []
    for row in es_data:
        data: dict[str, Any] = {'_index': index_name, '_id': row['uuid']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope="session")
def genres_index_settings():
    index = es_settings.genres_index_name
    mappings = es_settings.genres_mappings
    settings = es_settings.genres_settings

    return index, mappings, settings


@pytest_asyncio.fixture(scope="session")
def genres_route():
    return settings.genres_uri
