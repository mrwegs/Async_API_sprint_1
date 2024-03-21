from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.services.genre import GenreService, get_genre_service
from src.models.genre import Genre


router = APIRouter(
    tags=['genres'],
    responses={HTTPStatus.NOT_FOUND: {'description': 'Not found'}},
)

@router.get('/')
@cache(expire=30)
async def get_genres(
    genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:

    genres = await genre_service.get_genres_list()

    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return genres

@router.get('/{genre_id}')
@cache(expire=30)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_genre_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return genre