import pytest_asyncio
from redis.asyncio.client import Redis

from tests.functional.settings import settings


@pytest_asyncio.fixture(scope='session')
async def redis():
    redis = Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    yield redis
    await redis.close()