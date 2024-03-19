
from enum import Enum


class SortType(Enum):
    IMDB_ASC = '+imdb_rating'
    IMDB_DESC = '-imdb_rating'
    _SCORE_ASC = '+_score'
    _SCORE_DESC = '-_score'


class QueryContext(Enum):
    FILTER = 'filter'
    MATCH = 'match'


class TableFields(str, Enum):
    TITLE = 'title'
    GENRE = 'genre'
