from typing import Generic, Sequence

from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.core.query_builder.sortbuilder import SortQueryBuilder
from src.db.elastic import get_elastic
from src.core.types import Model
from src.core.query_builder.base import PaginationBuilder
from src.core.searcher.base import Searcher


class ElasticSearcher(Searcher, Generic[Model]):
    """
    The Elasticsearcher class defines the search logic for Elasticsearch.
    It provides a way to separate the search logic from the business logic of an application,
    which helps to improve maintainability and scalability.
    """

    def __init__(self, connection: AsyncElasticsearch) -> None:
        self._connection: AsyncElasticsearch = connection

    async def search(
            self,
            query_builder: PaginationBuilder,
            **kwargs
        ) -> Sequence[Model]:

        response: ObjectApiResponse[Model] = await self._connection.search(
            index=query_builder.index,
            from_=query_builder.from_,
            size=query_builder.page_size,
            source=query_builder.source
        )

        return [doc['_source'] for doc in response['hits']['hits']]

    async def get(self, key, **kwargs) -> Model:
        index_name = kwargs.get('index')
        if not index_name:
            raise ValueError('Index is required!')

        response: ObjectApiResponse[Model] = await self._connection.get(
            index=index_name,
            id=key
        )

        return response['_source']

class SortingSearcher(ElasticSearcher, Generic[Model]):
    """
    The SortingElasticsearcher class defines the search logic for
    Elasticsearch with sorting capabilities.
    It provides a way to separate the search logic from the business
    logic of an application,
    which helps to improve maintainability and scalability.
    """

    async def search_with_sorting(
            self,
            query_builder: SortQueryBuilder,
            **kwargs
        ) -> Sequence[Model]:

        response: ObjectApiResponse[Model] = await self._connection.search(
            index=query_builder.index,
            from_=query_builder.from_,
            size=query_builder.page_size,
            query=query_builder.query,
            sort=query_builder.sort,
            source=query_builder.source
        )

        return [doc['_source'] for doc in response['hits']['hits']]


async def get_searcher(
        es: AsyncElasticsearch = Depends(get_elastic)
) -> ElasticSearcher:
    return ElasticSearcher(es)


async def get_sorting_searcher(
        es: AsyncElasticsearch = Depends(get_elastic)
) -> SortingSearcher:
    return SortingSearcher(es)