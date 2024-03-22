from pydantic import UUID4

from src.models.dumps import BaseOrjsonModel


class Film(BaseOrjsonModel):
    """Класс для краткого описания Кинопроизведения"""
    uuid: str
    title: str | None
    description: str | None
    imdb_rating: float


class FilmResponse(BaseOrjsonModel):
    """Класс для описания фильма, передаваемого в ответе пользователю"""
    uuid: str
    title: str | None
    imdb_rating: float


class Model(BaseOrjsonModel):
    """Базовый класс для описания Персоналий"""
    uuid: UUID4
    name: str

    def __eq__(self, __other: 'Model') -> bool:
        return self.uuid == __other.uuid

    def __hash__(self) -> int:
        return self.uuid.int


class Actor(BaseOrjsonModel):
    """Класс для описания актера"""


class Writer(BaseOrjsonModel):
    """Класс для описания сценариста"""


class FilmDetails(BaseOrjsonModel):
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
