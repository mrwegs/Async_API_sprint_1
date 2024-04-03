from functools import lru_cache
from typing import Unpack

import elasticsearch
from fastapi import Depends

from src.api.v1.params import FilterParams
from src.core.config import settings
from src.core.query_builder.person import PersonQueryBuilder
from src.core.query_builder.sortbuilder import QueryRequest
from src.core.repository.base import Repository
from src.core.repository.redis import get_repo
from src.core.searcher.elastic import SortingSearcher, get_sorting_searcher
from src.models.film import FilmResponse
from src.models.person import Person


class PersonService:
    """
        The PersonService class provides an interface for retrieving person data from ElasticSearch.

        Args:
            redis (Redis): A Redis client for caching data.
            elastic (AsyncElasticsearch): An Elasticsearch client for querying data.
        """

    def __init__(self, repo: Repository, searcher: SortingSearcher):
        self.repo = repo
        self.searcher = searcher

    def __repr__(self):
        return self.__class__.__name__

    async def get_person_by_id(self, person_id: str) -> Person | None:
        try:
            person = await self.searcher.get(person_id, index=settings.persons_index)
        except elasticsearch.NotFoundError:
            person = None

        if not person:
            return None

        return Person(**person)

    async def get_persons_list(
            self,
            params: FilterParams,
            **query_request: Unpack[QueryRequest]
    ) -> list[Person] | None:
        searcher = PersonQueryBuilder(params, query_request)
        persons = await self.searcher.search_with_sorting(searcher)

        if not persons:
            return None

        return [Person(**doc) for doc in persons]

    async def get_persons_films(
            self,
            person_id: str
    ) -> list[FilmResponse] | None:

        person_data = await self.searcher.get(person_id, index=settings.persons_index)
        person = Person(**person_data)

        if not person:
            return None

        return [FilmResponse(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in
                person.films]


@lru_cache()
def get_person_service(
        repo: Repository = Depends(get_repo),
        searcher: SortingSearcher = Depends(get_sorting_searcher),
) -> PersonService:
    return PersonService(repo, searcher)
