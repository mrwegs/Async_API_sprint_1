from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query,
)
from pydantic import BaseModel

from src.services.enumtypes import QueryContext, TableFields
from src.services.film import get_film_service, FilmService
from src.models.film import FilmDetails
from src.api.v1.params import FilterParams, SearchParams

router = APIRouter(
    tags=['films'],
    responses={HTTPStatus.NOT_FOUND: {'description': 'Not found'}},
)


class FilmResponse(BaseModel):
    uuid: str
    title: str | None
    imdb_rating: float


@router.get('/search')
async def search_films_by_title(
        title: Annotated[str, Query(min_length=3)],
        params: SearchParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponse]:
    """Метод для поиска фильмов с по названию"""

    films = await film_service.get_films_list(
        params=params,
        context=QueryContext.MATCH,
        fields=[TableFields.TITLE],
        value=title
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmResponse(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get('/{film_id}', response_model=FilmDetails)
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
    ) -> FilmDetails:
    """Метод для получения полного описания фильма по идентификатору"""

    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return film


@router.get('')
async def get_films(
    genre: str | None = None,
    params: FilterParams = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:
    """Метод для получения списка фильмов с возможностью фильтации по жанру"""

    films = await film_service.get_films_list(
        params=params,
        context=QueryContext.FILTER,
        fields=[TableFields.GENRE],
        value=genre
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmResponse(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]
