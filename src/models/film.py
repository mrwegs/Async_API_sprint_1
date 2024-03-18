import orjson
from pydantic import UUID4, BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
    """Класс для краткого описания Кинопроизведения"""
    uuid: str
    title: str
    description: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Model(BaseModel):
    """Базовый класс для описания Персоналий"""
    uuid: UUID4
    name: str

    def __eq__(self, __other: 'Model') -> bool:
        return self.uuid == __other.uuid

    def __hash__(self) -> int:
        return self.uuid.int


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
