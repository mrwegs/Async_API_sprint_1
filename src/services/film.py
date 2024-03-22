from functools import lru_cache
from typing import Unpack

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from src.api.v1.params import FilterParams
from src.core.config import settings
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import Film, FilmDetails
from src.services.query_builder import (ESQueryBuilder, FilmQueryBuilder,
                                        QueryRequest)


class FilmService:
    """
        The FilmService class provides an interface for retrieving filmwork data from ElasticSearch.

        Args:
            redis (Redis): A Redis client for caching film data.
            elastic (AsyncElasticsearch): An Elasticsearch client for searching film data.
        """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> FilmDetails | None:
        film = await self._get_film_from_elastic(film_id)
        if not film:
            return None

        return film

    async def get_films_list(
            self,
            params: FilterParams,
            **query_request: Unpack[QueryRequest]
    ) -> list[Film]:

        searcher = FilmQueryBuilder(params, query_request)
        films = await self._get_films_list(searcher)

        return films

    async def _get_film_from_elastic(self, film_id: str) -> FilmDetails | None:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return FilmDetails(**doc['_source'])

    async def _get_films_list(self, searcher: ESQueryBuilder) -> list[Film]:
        films: list[Film] = []

        response = await self.elastic.search(
            index=settings.movies_index,
            from_=searcher.from_,
            size=searcher.page_size,
            query=searcher.query,
            sort=searcher.sort,
            source=searcher.source
        )

        for film in response['hits']['hits']:
            films.append(Film(**film['_source']))

        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
