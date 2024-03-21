from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache

from src.api.v1.params import FilterParams, SearchParams
from src.models.film import FilmDetails, FilmResponse
from src.services.enumtypes import FilmworkFields, QueryContext
from src.services.film import FilmService, get_film_service

router = APIRouter(
    tags=['films'],
    responses={HTTPStatus.NOT_FOUND: {'description': 'Not found'}},
)



@router.get('/search')
@cache(expire=30)
async def search_films_by_title(
        title: Annotated[str, Query(min_length=3)],
        params: SearchParams = Depends(),
        film_service: FilmService = Depends(get_film_service),
) -> list[FilmResponse]:
    """Метод для поиска фильмов по названию"""

    films = await film_service.get_films_list(
        params=params,
        context=QueryContext.MATCH,
        fields=[FilmworkFields.TITLE],
        value=title
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmResponse(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get('/{film_id}', response_model=FilmDetails)
@cache(expire=30)
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
@cache(expire=30)
async def get_films(
    genre: str | None = None,
    params: FilterParams = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:
    """Метод для получения списка фильмов с возможностью фильтации по жанру"""

    films = await film_service.get_films_list(
        params=params,
        context=QueryContext.FILTER,
        fields=[FilmworkFields.GENRE],
        value=genre
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmResponse(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in films]
