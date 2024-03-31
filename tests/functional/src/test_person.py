import pytest


@pytest.mark.asyncio
async def test_person(
        es_write_data,
        make_get_request,
        person_data,
        persons_index_settings
):
    index, mappings, settings = persons_index_settings
    await es_write_data(person_data, index, mappings, settings)
    item = person_data[0]
    uri = '/api/v1/persons/' + item['_id']
    body, status = await make_get_request(uri=uri)

    assert status == 200
    for film in item['_source']['films']:
        film.pop('title')
        film.pop('imdb_rating')
    assert body == item['_source']


@pytest.mark.asyncio
async def test_person_film(
        es_write_data,
        make_get_request,
        person_data,
        persons_index_settings
):
    index, mappings, settings = persons_index_settings
    await es_write_data(person_data, index, mappings, settings)

    item = person_data[0]
    uri = f'/api/v1/persons/{item['_id']}/film'
    body, status = await make_get_request(uri=uri)

    assert status == 200
    assert len(body) == 2
    assert body[0]['uuid'] == 'fb111f22-121e-44a7-b78f-b19191810fbf'


@pytest.mark.parametrize(
    'add_uri, expected_answer',
    [
        (
                {},
                {'status': 200, 'length': 3}
        ),
        (
                {'uri': '/film'},
                {'status': 200, 'length': 2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_person_cache(
        add_uri,
        expected_answer,
        es_write_data,
        es_delete_data,
        person_data,
        make_get_request,
        persons_index_settings
):
    index, mappings, settings = persons_index_settings
    await es_write_data(person_data, index, mappings, settings)

    item = person_data[0]
    uri = f'/api/v1/persons/{item['_id']}'
    if add_uri:
        uri += add_uri['uri']
    await make_get_request(uri=uri)
    await es_delete_data(id=item['_id'], index=index)

    body, status = await make_get_request(uri=uri)
    assert status == expected_answer['status']
    assert len(body) == expected_answer['length']
