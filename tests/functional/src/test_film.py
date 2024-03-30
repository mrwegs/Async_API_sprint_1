import pytest

from tests.functional.settings import es_settings

@pytest.mark.parametrize(
        'index_name',
        ['films', 'persons']
)
@pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (
                {'title': 'The Star'},
                {'status': 200, 'length': 50}
            ),
            (
                {'title': 'Mashed Potato'},
                {'status': 404, 'length': 1}
            )
        ]
)
@pytest.mark.asyncio
async def test_search(
    make_get_request,
    es_write_data,
    film_data,
    movies_index_settings,
    index_name,
    query_data,
    expected_answer
):
    index, mappings, settings = movies_index_settings

    await es_write_data(
        film_data,
        index,
        mappings,
        settings
    )

    body, status = await make_get_request(f'/api/v1/{index_name}/search', query_data)

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
