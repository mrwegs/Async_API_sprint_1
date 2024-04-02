from abc import ABC, abstractproperty
from copy import deepcopy
from typing import Any, Mapping

from src.api.v1.params import PageParams


class BaseBuilder(ABC):
    """BaseBuilder is an abstract class that provides a basic structure
    for building search queries for any search engines like Elasticsearch
    """

    _index: str
    _source: Mapping[str, Any]

    def __init__(self, params: PageParams) -> None:
        self._page_number = params.page_number
        self._page_size = params.page_size

    @property
    def from_(self) -> int:
        return (self._page_number - 1) * self._page_size

    @property
    def page_size(self) -> int:
        return self._page_size

    @abstractproperty
    def source(self) -> Mapping[str, Any]:
        raise NotImplementedError

    @abstractproperty
    def index(self) -> str:
        raise NotImplementedError


class PaginationBuilder(BaseBuilder):
    """Class for building pagination queries"""

    @property
    def source(self) -> Mapping[str, Any]:
        return deepcopy(self._source)

    @property
    def index(self) -> str:
        return self._index