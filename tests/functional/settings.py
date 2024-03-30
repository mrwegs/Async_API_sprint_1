from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    redis_host: str = ...
    redis_port: int = 6379
    redis_db: int = 2

    elastic_host: str = ...
    elastic_port: int = 9200
    es_movies_index: str = 'movies'

    async_api_host: str = ...
    async_api_port: int = 8000
    api_movies_endpoint: str = '/api/v1/films'


test_settings = Settings()
