from typing import Any, Mapping

from src.core.query_builder.sortbuilder import SortQueryBuilder
from src.core.config import settings


class FilmQueryBuilder(SortQueryBuilder):
    """
    The FilmQueryBuilder class inherits from the SortQueryBuilder class and
    overrides the _source and _index properties to specify the fields to include
    in the search query and the index to search, respectively.
    """

    _source: Mapping[str, Any] = {
        'includes': ['uuid', 'title', 'description', 'imdb_rating']
    }
    _index: str = settings.movies_index
