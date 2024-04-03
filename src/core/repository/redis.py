from functools import lru_cache
from typing import Generic

from fastapi import Depends
from redis.asyncio import Redis

from src.core.repository.base import Repository
from src.core.types import Model
from src.db.redis import get_redis


class RedisRepo(Repository, Generic[Model]):
    """
    A repository class that uses Redis as its data store.

    Args:
        connection (Redis): A Redis connection object.

    Attributes:
        _redis (Redis): A Redis connection object.
    """

    def __init__(self, connection: Redis) -> None:
        self._redis: Redis = connection

    async def get(self, key) -> Model:
        result = await self._connection.get(key)

        return result

    async def put(self, key, value) -> None:
        await self._connection.set(key, value)


@lru_cache()
def get_repo(
    redis: Redis = Depends(get_redis)
) -> RedisRepo:
    return RedisRepo(redis)