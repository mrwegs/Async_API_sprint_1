from typing import Generic
from redis.asyncio import Redis

from src.db.redis import get_redis
from src.core.repository.base import Repository
from src.core.types import Model


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


async def get_repo() -> RedisRepo:
    return RedisRepo(await get_redis())