import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'../.env', env_file_encoding='utf-8', extra='ignore')

    project_name: str = 'movies'
    redis_host: str = '127.0.0.1'
    redis_port: int = ...
    redis_db: int = Field(..., alias='REDIS_ASYNC_API_DB')
    cache_expire: int = Field(..., alias='FILM_CACHE_EXPIRE_IN_SECONDS')

    elastic_host: str = '127.0.0.1'
    elastic_port: int = 9200
    elastic_url: str = Field(..., alias='ES_URL')

    max_page_size: int = ...
    movies_index: str = 'movies'
    genres_index: str = 'genres'
    persons_index: str = 'persons'


settings = Setting()
