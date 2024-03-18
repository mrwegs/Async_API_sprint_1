from typing import Any, TypedDict

from src.api.v1.params import Params
from src.services.enumtypes import QueryContext


class QueryRequest(TypedDict):
    context: QueryContext
    fields: list[str]
    value: Any 


class ESQueryBuilder:
    __query_base = {'bool': {}}

    def __init__(
            self,
            params: Params,
            request: QueryRequest,
    ) -> None:
        
        self._page_number = params.page_number
        self._page_size = params.page_size
        self._sort = params.sort
        self._context = request['context']
        self._fields = request['fields']
        self._value = request['value']
    
    def _build_match(self) -> None:
        match_list = []
        for field in self._fields:
            match = {'match': {field: self._value}}
            match_list.append(match)
        
        self.__query_base['bool']['must'] = match_list
    
    def _build_filter(self) -> None:
        filter_list = []
        for field in self._fields:
            filter = {'term': {field: self._value}}
            filter_list.append(filter)
        
        self.__query_base['bool']['filter'] = filter_list

    @property
    def query(self) -> dict:
        if self._context is QueryContext.MATCH:
            self._build_match()
        elif self._context is QueryContext.FILTER:
            self._build_filter
        
        return self.__query_base

    @property
    def sort(self) -> list[dict] | None:
        pass

    @property
    def from_(self) -> int:
        return (self._page_number - 1) * self._page_size
