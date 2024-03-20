from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.v1.films import FilmResponse
from src.services.enumtypes import PersonFields, QueryContext
from src.services.person import PersonService, get_person_service
from src.api.v1.params import FilterParams, SearchParams
from src.models.person import Person


router = APIRouter(
    tags=['persons'],
    responses={HTTPStatus.NOT_FOUND: {'description': 'Not found'}},
)

@router.get('/search')
async def search_persons(
    name: Annotated[str, Query(min_length=3)],
    params: SearchParams = Depends(),
    person_service: PersonService = Depends(get_person_service)
) -> list[Person]:

    persons = await person_service.get_persons_list(
        params=params,
        context=QueryContext.MATCH,
        fields=[PersonFields.FULL_NAME],
        value=name
    )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return persons

@router.get('/{person_id}')
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> Person:

    person = await person_service.get_person_by_id(person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return person


@router.get('/{person_id}/film')
async def get_films_by_person(
    person_id: str,
    params: FilterParams = Depends(),
    person_service: PersonService = Depends(get_person_service)
) -> list[FilmResponse]:

    films = await person_service.get_persons_films(
        person_id=person_id
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return films
