import pytest

from tests.functional.settings import es_settings, settings


@pytest.mark.parametrize(
    "query_data, expected_answer, api_route",
    [
        (
            {"title": "The Star", "page_size": 20},
            {"status": 200, "length": 20},
            settings.films_uri,
        ),
        (
            {"title": "The Test"},
            {"status": 404, "length": 1},
            settings.films_uri,
        ),
        (
            {"name": "Anna De Armas", "page_size": 20},
            {"status": 200, "length": 20},
            settings.persons_uri
        ),
        (
            {"name": "Test Testov"},
            {"status": 404, "length": 1},
            settings.persons_uri
        ),
    ],
)
@pytest.mark.asyncio
async def test_search(
    upload_data_to_es,
    query_data,
    expected_answer,
    make_get_request,
    api_route,
):
    body, status = await make_get_request(api_route + '/search', query_data)

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
        'query_data, expected_answer, index, api_route',
        [
            (
                {'title': 'The Star', 'page_size': 20},
                {'status': 200, 'length': 20},
                es_settings.movies_index_name,
                settings.films_uri,
            ),
            (
                {'name': 'Anna De Armas', 'page_size': 20},
                {'status': 200, 'length': 20},
                es_settings.persons_index_name,
                settings.persons_uri,
            ),
        ]
)
@pytest.mark.asyncio
async def test_redis_cache(
    es,
    upload_data_to_es,
    query_data,
    expected_answer,
    make_get_request,
    index,
    api_route
):
    await make_get_request(api_route + '/search', query_data)
    await es.indices.delete(index=index)

    body, status = await make_get_request(api_route + '/search', query_data)

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
