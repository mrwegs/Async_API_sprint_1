import pytest
from tests.functional.settings import settings


@pytest.mark.parametrize(
    'api_route',
    [
        settings.films_uri,
        settings.genres_uri,
    ]
)
@pytest.mark.parametrize(
    'query_data',
    [
        {'page_size': -1},
        {'page_number': -1},
        {'page_number': 9999999},
        {'page_size': 9999999},

    ]
)
@pytest.mark.asyncio
async def test_unprocessable_entity(
    upload_data_to_es,
    make_get_request,
    query_data,
    api_route
):

    _, status = await make_get_request(api_route, query_data)

    assert status == 422


@pytest.mark.parametrize(
    'api_route',
    [
        settings.films_uri + '/search',
        settings.persons_uri + '/search',
    ]
)
@pytest.mark.parametrize(
    'query_data',
    [
        {'search_field': "Test", 'page_size': -1},
        {'search_field': "Test", 'page_number': -1},
        {'search_field': "Test", 'page_number': 9999999},
        {'search_field': "Test", 'page_size': 9999999},
        {'search_field': 'Test', 'sort': 'test_test'}

    ]
)
@pytest.mark.asyncio
async def test_unprocessable_entity_search(
    upload_data_to_es,
    make_get_request,
    query_data,
    api_route
):
    _, status = await make_get_request(api_route, query_data)

    assert status == 422
