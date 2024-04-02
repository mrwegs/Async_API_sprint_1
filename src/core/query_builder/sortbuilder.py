from typing import Any, TypedDict

from src.core.query_builder.base import PaginationBuilder
from src.api.v1.params import FilterParams
from src.services.enumtypes import QueryContext, TableFields


class QueryRequest(TypedDict):
    """Bunch of input parameters for building a query

    Args:
    context: QueryContext
    context: Elasticsearch context for build filter query or matching query

    fields: list[TableFields]
    fields: list of column names for filtering

    value: query value
    """
    context: QueryContext
    fields: list[TableFields]
    value: Any


class SortQueryBuilder(PaginationBuilder):
    """Class for building queries provides sorting functionality"""

    _type_mapping = {'+': 'asc', '-': 'desc'}

    def __init__(
            self,
            params: FilterParams,
            request: QueryRequest,
    ) -> None:

        self._page_number = params.page_number
        self._page_size = params.page_size
        self._sort = params.sort.value
        self._context = request['context']
        self._fields = request['fields']
        self._value = request['value']
        self._query_base = {'bool': {}}

    def _build_match(self) -> None:
        match_list = []
        for field in self._fields:
            match = {'match': {field: self._value}}
            match_list.append(match)

        self._query_base['bool']['must'] = match_list

    def _build_filter(self) -> None:
        filter_list = []
        for field in self._fields:
            filter = {'term': {field: self._value}}
            filter_list.append(filter)

        self._query_base['bool']['filter'] = filter_list

    @property
    def query(self) -> dict:
        if self._value is None:
            pass
        elif self._context is QueryContext.MATCH:
            self._build_match()
        elif self._context is QueryContext.FILTER:
            self._build_filter()

        return self._query_base

    @property
    def sort(self) -> list[dict]:
        t, field = self._sort[0], self._sort[1:]

        return [{field: {'order': self._type_mapping[t]}}]