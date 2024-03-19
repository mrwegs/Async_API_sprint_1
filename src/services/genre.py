from functools import lru_cache
from fastapi import Depends
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.core.config import GENRES_INDEX
from src.models.genre import Genre


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_genres_list(self) -> list[Genre] | None:
        genres = await self._get_genres_list()
        if not genres:
            return None

        return genres

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