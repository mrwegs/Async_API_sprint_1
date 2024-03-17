from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
)
from pydantic import BaseModel

from src.services.film import get_film_service, FilmService
from src.api.v1.params import Params

router = APIRouter(
    tags=['films'],
    responses={HTTPStatus.NOT_FOUND: {'description': 'Not found'}},
)


class FilmResponse(BaseModel):
    id: str
    title: str


@router.get('/search')
async def search_films(
        title_query: Annotated[str | None, Query(min_length=3)],
        params: Params = Depends(),
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:

    films = await film_service.get_films_list(params=params, title_query=title_query)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmResponse(id=film.id, title=film.title) for film in films]


@router.get('/{film_id}', response_model=FilmResponse)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmResponse:

    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return FilmResponse(id=film.id, title=film.title)


@router.get('')
async def get_films(
    genre: str = None,
    params: Params = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:

    films = await film_service.get_films_list(params=params, genre=genre)

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmResponse(id=film.id, title=film.title) for film in films]
