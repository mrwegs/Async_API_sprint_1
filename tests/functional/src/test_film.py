import pytest

from tests.functional.settings import es_settings

# @pytest.mark.parametrize(
#         'route_type',
#         ['films', 'persons']
# )
# @pytest.mark.parametrize(
#         'query_data, expected_answer',
#         [
#             (
#                 {'title': 'The Star'},
#                 {'status': 200, 'length': 50}
#             ),
#             (
#                 {'title': 'Mashed Potato'},
#                 {'status': 404, 'length': 1}
#             )
#         ]
# )
# @pytest.mark.asyncio
# async def test_search(
#     make_get_request,
#     es_write_data,
#     film_data,
#     movies_index_settings,
#     # route_type,
#     query_data,
#     expected_answer
# ):
#     index, mappings, settings = movies_index_settings

#     await es_write_data(
#         film_data,
#         index,
#         mappings,
#         settings
#     )

#     body, status = await make_get_request('/api/v1/films/search', query_data)

#     assert status == expected_answer['status']
#     assert len(body) == expected_answer['length']


@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'title': 'The Star', 'page_size': 20},
            {'status': 200, 'length': 20}
        ),
        (
            {'title': 'The Star', 'page_number': 9999999},
            {'status': 404, 'length': 1}
        ),
        (
            {'title': 'The Star', 'page_size': 9999999},
            {'status': 422, 'length': 1}
        ),
        (
            {'title': 'Y'},
            {'status': 422, 'length': 1}
        ),
        (
            {'title': 'The Star', 'sort': 'dzhigurda'},
            {'status': 422, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_searh_films(
    make_get_request,
    es_write_data,
    film_data,
    movies_index_settings,
    params,
    expected_answer
):
    index, mappings, settings = movies_index_settings

    es_write_data(
        film_data,
        index,
        mappings,
        settings
    )

    body, status = await make_get_request('/api/v1/films/search', params)

    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
