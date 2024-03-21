from enum import Enum


class SortType(Enum):
    """Типы сортировки данных в ответе пользователю"""
    IMDB_ASC = '+imdb_rating'
    IMDB_DESC = '-imdb_rating'
    _SCORE_ASC = '+_score'
    _SCORE_DESC = '-_score'


class QueryContext(Enum):
    """Контекст поиска данных в ElasticSearch"""
    FILTER = 'filter'
    MATCH = 'match'


class TableFields(str, Enum):
    """Класс для описания полей индексов ElasticSearch"""
    ...


class FilmworkFields(TableFields):
    """Класс для описания полей индекса фильмов ElasticSearch"""
    TITLE = 'title'
    GENRE = 'genre'


class PersonFields(TableFields):
    """Класс для описания полей индекса персоналий ElasticSearch"""
    FULL_NAME = 'full_name'
