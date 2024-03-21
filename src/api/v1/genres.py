from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.core import config
from src.models.genre import Genre
from src.services.genre import GenreService, get_genre_service

router = APIRouter(
    tags=['genres'],
    responses={HTTPStatus.NOT_FOUND: {'description': 'Not found'}},
)

@router.get('/')
@cache(expire=config.FILM_CACHE_EXPIRE_IN_SECONDS)
async def get_genres(
    genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    """Метод для получения списка жанров"""

    genres = await genre_service.get_genres_list()

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return genres

@router.get('/{genre_id}')
@cache(expire=config.FILM_CACHE_EXPIRE_IN_SECONDS)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    """Метод для получения полного описания жанра по идентификатору"""

    genre = await genre_service.get_genre_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return genre