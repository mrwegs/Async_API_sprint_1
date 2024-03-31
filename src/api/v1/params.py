from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from src.core.config import settings
from src.services.enumtypes import SortType


class PageParams(BaseModel):
    """Класс для описания параметров страницы"""

    page_size: Annotated[int, Query(gt=0, lt=settings.max_page_size)] = 50
    page_number: Annotated[int, Query(gt=0, lt=10000 / settings.max_page_size)] = 1


class FilterParams(PageParams):
    """Класс для описания параметров страницы с сортировкой по рейтингу"""
    sort: SortType = SortType.IMDB_DESC


class SearchParams(FilterParams):
    """Класс для описания параметров страницы с сортировкой по релевантности"""
    sort: SortType = SortType._SCORE_DESC
