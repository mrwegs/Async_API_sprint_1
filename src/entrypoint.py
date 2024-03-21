import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.api.v1.films import router as films_router
from src.api.v1.genres import router as genres_router
from src.api.v1.persons import router as persons_router
from src.core import config
from src.core.logger import LOGGING
from src.db import elastic, redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = aioredis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_ASYNC_API_DB)
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
    FastAPICache.init(RedisBackend(redis.redis), prefix="fastapi-cache")
    yield
    await redis.redis.close()
    await elastic.es.close()

app = FastAPI(
    title=config.PROJECT_NAME,
    lifespan=lifespan,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(films_router, prefix='/api/v1/films')
app.include_router(genres_router, prefix='/api/v1/genres')
app.include_router(persons_router, prefix='/api/v1/persons')


@app.get('/')
def index():
    return {'hello': 'world'}


if __name__ == '__main__':
    uvicorn.run(
        'src.entrypoint:app',
        host='0.0.0.0',
        port=8000,
    )
