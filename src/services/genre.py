from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from redis.asyncio import Redis

from src.core.config import GENRES_INDEX
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre


class GenreService:
    """
        The GenreService class provides an interface for retrieving genre data from ElasticSearch.

        Args:
            redis (Redis): The Redis client used for caching data.
            elastic (AsyncElasticsearch): The Elasticsearch client used for storing and retrieving data.
        """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._get_genre_by_id(genre_id)
        return genre

    async def get_genres_list(self) -> list[Genre] | None:
        genres = await self._get_genres_list()
        if not genres:
            return None

        return genres

    async def _get_genre_by_id(self, genre_id: str) -> Genre | None:
        response = await self.elastic.get(
            index=GENRES_INDEX,
            id=genre_id
        )

        if not response:
            return None

        return Genre(**response['_source'])

    async def _get_genres_list(self) -> list[Genre]:
        genres_list = []
        response = await self.elastic.search(index=GENRES_INDEX)

        for genre in response['hits']['hits']:
            genres_list.append(Genre(**genre['_source']))

        return genres_list


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)