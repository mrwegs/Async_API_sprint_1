import pytest


@pytest.mark.asyncio
async def test_genre_by_id(
    genre_data,
    make_get_request,
    es_write_data,
    genres_index_settings,
    genres_route
):
    await es_write_data(genre_data, *genres_index_settings)
    doc = genre_data[0]

    url = genres_route + f'/{doc["_id"]}'
    body, status = await make_get_request(url)

    assert status == 200
    assert body == doc['_source']


@pytest.mark.asyncio
async def test_genre_not_found(
    genre_data,
    make_get_request,
    es_write_data,
    genres_index_settings,
    genres_route
):
    await es_write_data(genre_data, *genres_index_settings)

    url = genres_route + '/test'
    _, status = await make_get_request(url)

    assert status == 404


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'page_size': 20},
         {'status': 200, 'length': 20})
    ]
)
@pytest.mark.asyncio
async def test_genres(
    genre_data,
    es_write_data,
    make_get_request,
    genres_index_settings,
    genres_route,
    query_data,
    expected_answer
):

    await es_write_data(genre_data, *genres_index_settings)

    body, status = await make_get_request(genres_route, query_data)

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']