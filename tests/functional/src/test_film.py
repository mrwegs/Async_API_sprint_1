import pytest


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {},
                {'status': 200, 'length': 50}
        ),
        (
                {'page_size': 7},
                {'status': 200, 'length': 7}
        ),
        (
                {'page_size': 17},
                {'status': 200, 'length': 17}
        ),
        (
                {'page_size': 0},
                {'status': 422, 'length': 1}
        ),
        (
                {'genre': 'Action'},
                {'status': 200, 'length': 50}
        ),
        (
                {'genre': 'Action', 'page_size': 12},
                {'status': 200, 'length': 12}
        ),
        (
                {'genre': 'Sci-Fi'},
                {'status': 200, 'length': 50}
        ),
        (
                {'genre': 'Sci-Fi', 'page_size': 15},
                {'status': 200, 'length': 15}
        ),
        (
                {'genre': 'Drama'},
                {'status': 404, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_films(
        query_data,
        expected_answer,
        es_write_data,
        make_get_request,
        film_data,
        movies_index_settings
):
    index, mappings, settings = movies_index_settings
    await es_write_data(
        data=film_data,
        index=index,
        mappings=mappings,
        settings=settings
    )

    body, status = await make_get_request(uri='/api/v1/films/', data=query_data)

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']


@pytest.mark.asyncio
async def test_film_item(
        es_write_data,
        make_get_request,
        film_data,
        movies_index_settings
):
    index, mappings, settings = movies_index_settings
    await es_write_data(
        data=film_data,
        index=index,
        mappings=mappings,
        settings=settings
    )
    item = film_data[0]
    uri = '/api/v1/films/' + item['_id']
    body, status = await make_get_request(uri=uri)

    assert status == 200
    assert item['_source'] == body


@pytest.mark.asyncio
async def test_film_cache(
        es_write_data,
        es_delete_data,
        make_get_request,
        film_data,
        movies_index_settings
):
    index, mappings, settings = movies_index_settings
    await es_write_data(
        data=film_data,
        index=index,
        mappings=mappings,
        settings=settings
    )
    item = film_data[0]
    uri = '/api/v1/films/' + item['_id']
    await make_get_request(uri=uri)
    await es_delete_data(id=item['_id'], index=index)

    body, status = await make_get_request(uri=uri)
    assert status == 200
    assert item['_source'] == body
