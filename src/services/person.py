from functools import lru_cache
from typing import Unpack

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from src.api.v1.params import FilterParams
from src.core.config import PERSONS_INDEX
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.film import FilmResponse
from src.models.person import Person
from src.services.query_builder import (ESQueryBuilder, PersonQueryBuilder,
                                        QueryRequest)


class PersonService:
    """
        The PersonService class provides an interface for retrieving person data from ElasticSearch.

        Args:
            redis (Redis): A Redis client for caching data.
            elastic (AsyncElasticsearch): An Elasticsearch client for querying data.
        """
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_person_by_id(self, person_id: str) -> Person | None:
        person = await self._get_person_from_elastic(person_id)

        return person

    async def get_persons_list(
            self,
            params: FilterParams,
            **query_request: Unpack[QueryRequest]
    ) -> list[Person]:
        searcher = PersonQueryBuilder(params, query_request)
        persons = await self._get_persons_from_elastic(searcher)

        return persons

    async def get_persons_films(
        self,
        person_id: str
    ) -> list[FilmResponse] | None:

        person_data: Person | None = await self._get_person_from_elastic(person_id)
        if not person_data:
            return None

        return [FilmResponse(uuid=film.uuid, title=film.title, imdb_rating=film.imdb_rating) for film in person_data.films]


    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            person = await self.elastic.get(index=PERSONS_INDEX, id=person_id)
        except NotFoundError:
            return None

        return Person(**person['_source'])

    async def _get_persons_from_elastic(self, searcher: ESQueryBuilder) -> list[Person]:
        films = []

        response = await self.elastic.search(
            index=searcher.index,
            from_=searcher.from_,
            size=searcher.page_size,
            query=searcher.query,
            sort=searcher.sort,
        )

        for film in response['hits']['hits']:
            films.append(Person(**film['_source']))

        return films


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:

    return PersonService(redis, elastic)
