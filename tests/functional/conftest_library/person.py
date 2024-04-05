import uuid

import pytest_asyncio

from tests.functional.settings import es_settings, settings


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
def persons_route():
    return settings.persons_uri
