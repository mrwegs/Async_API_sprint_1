import orjson
from pydantic import BaseModel

from src.models.dumps import orjson_dumps

class PersonsFilms(BaseModel):
    """Класс для описани фильмов с участием конкретной персоны"""
    uuid: str
    roles: list[str]
    title: str = ''
    imdb_rating: float = 0.0

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

class PersonsFilmsResponse(BaseModel):
    """Класс для описани фильмов с участием конкретной персоны"""
    uuid: str
    roles: list[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

class Person(BaseModel):
    """Класс для описания персоналий"""
    uuid: str
    full_name: str
    films: list[PersonsFilms]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

class PersonResponse(BaseModel):
    """Класс для описания персоналий"""
    uuid: str
    full_name: str
    films: list[PersonsFilmsResponse]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps