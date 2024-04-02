from functools import lru_cache

from fastapi import Depends

from src.core.query_builder.genre import GenreQueryBuilder
from src.core.repository.redis import get_repo
from src.core.searcher.elastic import get_searcher
from src.api.v1.params import PageParams
from src.core.repository.base import Repository
from src.core.searcher.base import Searcher
from src.models.genre import Genre
from src.core.config import settings


class GenreService:
    """
        The GenreService class provides an interface for retrieving genre data from ElasticSearch.

        Args:
            redis (Redis): The Redis client used for caching data.
            elastic (AsyncElasticsearch): The Elasticsearch client used for storing and retrieving data.
        """

    def __init__(self, repo: Repository, searcher: Searcher):
        self.repo = repo
        self.searcher = searcher

    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        genre = await self.searcher.get(genre_id, index=settings.genres_index)

        if not genre:
            return None

        return Genre(**genre)

    async def get_genres_list(
            self,
            params: PageParams,
        ) -> list[Genre] | None:

        query_builder = GenreQueryBuilder(params)
        genres = await self.searcher.search(query_builder)

        if not genres:
            return None

        return genres


@lru_cache()
def get_genre_service(
        repo: Repository = Depends(get_repo),
        searcher: Searcher = Depends(get_searcher),
) -> GenreService:
    return GenreService(repo, searcher)