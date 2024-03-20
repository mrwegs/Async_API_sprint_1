import orjson
from pydantic import BaseModel

from src.models.dumps import orjson_dumps


class Genre(BaseModel):
    """Класс для описания жанра"""

    uuid: str
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps