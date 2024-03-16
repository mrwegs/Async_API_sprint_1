from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class SettingsDB(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    CHUNK: int


class SettingsRedis(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int


class SettingsES(BaseSettings):
    ES_HOST: str
    ES_PORT: int
    INDEX_NAMES: str
    INTERVAL: int

    @field_validator('INDEX_NAMES')
    @classmethod
    def split_index_names(cls, value):
        return value.split(',')


settings_db = SettingsDB()
settings_redis = SettingsRedis()
settings_es = SettingsES()
