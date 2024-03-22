from src.models.dumps import BaseOrjsonModel


class PersonsFilms(BaseOrjsonModel):
    """Класс для описани фильмов с участием конкретной персоны"""
    uuid: str
    roles: list[str]
    title: str = ''
    imdb_rating: float = 0.0


class PersonsFilmsResponse(BaseOrjsonModel):
    """Класс для описани фильмов с участием конкретной персоны,
    отправляемый в ответе пользователю"""
    uuid: str
    roles: list[str]


class Person(BaseOrjsonModel):
    """Класс для описания персоналий"""
    uuid: str
    full_name: str
    films: list[PersonsFilms]


class PersonResponse(BaseOrjsonModel):
    """Класс для описания персоналий, отправляемый в ответе пользователю"""
    uuid: str
    full_name: str
    films: list[PersonsFilmsResponse]
