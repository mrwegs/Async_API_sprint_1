
from enum import Enum


class SortType(Enum):
    IMDB_ASC = '+imdb_rating'
    IMDB_DESC = '-imdb_rating'


class QueryContext(Enum):
    FILTER = 'filter'
    MATCH = 'match'