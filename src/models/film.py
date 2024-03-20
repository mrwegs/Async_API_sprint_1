import orjson
from pydantic import UUID4, BaseModel

from src.models.dumps import orjson_dumps

class Film(BaseModel):
    """Класс для краткого описания Кинопроизведения"""
    uuid: str
    title: str | None
    description: str | None
    imdb_rating: float

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmResponse(BaseModel):
    uuid: str
    title: str | None
    imdb_rating: float


class Model(BaseModel):
    """Базовый класс для описания Персоналий"""
    uuid: UUID4
    name: str

    def __eq__(self, __other: 'Model') -> bool:
        return self.uuid == __other.uuid

    def __hash__(self) -> int:
        return self.uuid.int

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Actor(Model):
    """Класс для описания актера"""


class Writer(Model):
    """Класс для описания сценариста"""


class FilmDetails(BaseModel):
    """Класс для полного описания Кинопроизведения"""
    uuid: str
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: list[str]
    actors: list[Actor]
    writers: list[Writer]
    actors_names: list[str]
    writers_names: list[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
