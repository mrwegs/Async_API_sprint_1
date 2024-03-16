from http import HTTPStatus

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)
from pydantic import BaseModel

from src.services.film import get_film_service, FilmService
from src.api.v1.params import Params

router = APIRouter()


class FilmResponse(BaseModel):
    id: str
    title: str


@router.get('/{film_id}', response_model=FilmResponse)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmResponse:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmResponse(id=film.id, title=film.title)


# @router.get('/', response_model=list[FilmResponse])
# async def film_main(
#     params: Params = Depends(),
#     film_service: FilmService = Depends(get_film_service)
# ) -> list[FilmResponse]:
#     ...


@router.get('')
async def get_films(
    genre: str = None,
    params: Params = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:

    films = await film_service.get_films_list(params, genre)

    return [FilmResponse(id=film.id, title=film.title) for film in films]


@router.get('/search')
async def get_films_by_title(
        title_query: str,
        params: Params = Depends(),
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmResponse]:
    ...
