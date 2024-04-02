from typing import Any, Mapping

from src.core.query_builder.base import PaginationBuilder
from src.core.config import settings


class GenreQueryBuilder(PaginationBuilder):
    """
    The GenreQueryBuilder class inherits from the PaginationBuilder class and
    overrides the _source and _index properties to specify the fields to include
    in the search query and the index to search, respectively.
    """
    _index: str = settings.genres_index
    _source: Mapping[str, Any] = {
        'includes': ['uuid', 'name']
    }