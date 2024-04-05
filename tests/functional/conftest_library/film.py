import uuid

import pytest_asyncio

from tests.functional.settings import es_settings, settings


@pytest_asyncio.fixture(scope="session")
def film_data():
    index_name = es_settings.movies_index_name

    # 1. Генерируем данные для ES
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
        data = {'_index': index_name, '_id': row['uuid']}
        data.update({'_source': row})
        bulk_query.append(data)

    return bulk_query


@pytest_asyncio.fixture(scope="session")
def films_route():
    return settings.films_uri


@pytest_asyncio.fixture(scope="session")
def movies_index_settings():
    index = es_settings.movies_index_name
    mappings = es_settings.movies_mappings
    settings = es_settings.movies_settings

    return index, mappings, settings
