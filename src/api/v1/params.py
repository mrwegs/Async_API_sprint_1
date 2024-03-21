from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.core.config import MAX_PAGE_SIZE
from src.services.enumtypes import SortType


class PageParams(BaseModel):
    page_size: Annotated[int, Query(gt=0, lt=MAX_PAGE_SIZE)] = 50
    page_number: Annotated[int, Query(gt=0)] = 1


class FilterParams(PageParams):
    sort: SortType = SortType.IMDB_DESC


class SearchParams(FilterParams):
    sort: SortType = SortType._SCORE_DESC