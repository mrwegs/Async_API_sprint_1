from functools import lru_cache
from typing import Unpack

import elasticsearch
from fastapi import Depends

from src.core.repository.redis import get_repo
from src.core.searcher.elastic import SortingSearcher, get_sorting_searcher
from src.api.v1.params import FilterParams
from src.core.config import settings
from src.core.repository.base import Repository
from src.models.film import Film, FilmDetails
from src.core.query_builder.sortbuilder import QueryRequest
from src.core.query_builder.film import FilmQueryBuilder


class FilmService:
    """
        The FilmService class provides an interface for retrieving filmwork data from ElasticSearch.

        Args:
            redis (Redis): A Redis client for caching film data.
            elastic (AsyncElasticsearch): An Elasticsearch client for searching film data.
        """

    def __init__(self, repo: Repository, searcher: SortingSearcher):
        self.repo = repo
        self.searcher = searcher

    async def get_by_id(self, film_id: str) -> FilmDetails | None:
        try:
            film = await self.searcher.get(film_id, index=settings.movies_index)
        except elasticsearch.NotFoundError:
            film = None

        if not film:
            return None

        return FilmDetails(**film)

    async def get_films_list(
            self,
            params: FilterParams,
            **query_request: Unpack[QueryRequest]
    ) -> list[Film] | None:

        query_builder = FilmQueryBuilder(params, query_request)
        films = await self.searcher.search_with_sorting(query_builder)

        if not films:
            return None

        return [Film(**doc) for doc in films]


@lru_cache()
def get_film_service(
        repo: Repository = Depends(get_repo),
        searcher: SortingSearcher = Depends(get_sorting_searcher),
) -> FilmService:
    return FilmService(repo, searcher)
