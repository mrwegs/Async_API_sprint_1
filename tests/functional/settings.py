from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from tests.functional.testdata.es_mapping import (
    GENRES,
    GENRES_SETTINGS,
    MOVIES,
    MOVIES_SETTINGS,
    PERSONS,
    PERSONS_SETTINGS
)


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='tests/functional/.env', env_file_encoding='utf-8', extra='ignore')


class ESIndexSettings(EnvSettings):
    movies_index_name: str = Field(default=...)
    genres_index_name: str = Field(default=...)
    persons_index_name: str = Field(default=...)

    index_list: list[str] = [str(movies_index_name), str(persons_index_name), str(genres_index_name)]

    movies_mappings: dict = MOVIES
    genres_mappings: dict = GENRES
    persons_mappings: dict = PERSONS
    movies_settings: dict = MOVIES_SETTINGS
    genres_settings: dict = GENRES_SETTINGS
    persons_settings: dict = PERSONS_SETTINGS


class Settings(EnvSettings):
    redis_host: str = Field(default=...)
    redis_port: int = Field(default=...)
    redis_db: int = Field(default=...)

    elastic_host: str = Field(default=...)
    elastic_port: int = Field(default=...)

    async_api_host: str = Field(default=...)
    async_api_port: int = Field(default=...)

    service_url: str = f'http://{async_api_host}:{async_api_port}'

    persons_uri: str = '/api/v1/persons'
    films_uri: str = '/api/v1/films'
    genres_uri: str = '/api/v1/genres'


settings = Settings()

es_settings = ESIndexSettings()

dev_settings = Settings(
    redis_host='127.0.0.1',
    elastic_host='127.0.0.1',
    async_api_host='l127.0.0.1',
    service_url='http://127.0.0.1:80'
)
