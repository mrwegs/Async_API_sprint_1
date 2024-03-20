from typing import Any, Mapping, TypedDict

from src.api.v1.params import FilterParams
from src.services.enumtypes import QueryContext, TableFields


class QueryRequest(TypedDict):
    context: QueryContext
    fields: list[TableFields]
    value: Any


class ESQueryBuilder:
    _query_base = {'bool': {}}
    _type_mapping = {'+': 'asc', '-': 'desc'}
    _film_source: Mapping[str, Any] = {
        'includes': ['uuid', 'title', 'description', 'imdb_rating']
    }


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

    @property
    def from_(self) -> int:
        return (self._page_number - 1) * self._page_size

    @property
    def page_size(self) -> int:
        return self._page_size

    @property
    def source(self) -> Mapping[str, Any]:
        return self._film_source