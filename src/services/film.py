from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film
from src.core.config import FILM_CACHE_EXPIRE_IN_SECONDS, MOVIES_INDEX
from src.api.v1.params import Params
from src.services.searcher import ESSearcher


class FilmService:
    film_source: list[str] = ['id', 'title', 'description']

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_films_list(
            self,
            params: Params,
            genre: str | None = None,
            title_query: str | None = None
    ) -> list[Film]:

        searcher = ESSearcher(params, genre, title_query)
        films = await self._get_films_list(searcher)

        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _get_films_list(self, searcher: ESSearcher) -> list[Film]:
        films: list[Film] = []

        response = await self.elastic.search(
            index=MOVIES_INDEX,
            from_=searcher.from_,
            size=searcher.page_size,
            query=searcher.query,
            sort=searcher.sort,
            source=self.film_source,
        )

        for film in response['hits']['hits']:
            films.append(Film(**film['_source']))

        return films

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.model_validate_json(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _generate_id(
            self,
            params: Params,
            genre: str | None = None,
            query: str | None = None
    ):
        """Метод для генерации идентификатора для сохранения данных о фильмах в кеш."""
        return 1


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
