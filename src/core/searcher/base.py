from abc import ABC, abstractmethod
from typing import Generic

from src.core.types import Model


class Searcher(ABC, Generic[Model]):
    """
    The Searcher class defines an abstract interface for searching
    over a data store.
    It provides a way to separate the search logic from the business
    logic of an application,
    which helps to improve maintainability and scalability.

    The Searcher class is generic, allowing it to be used with
    different types of data models.
    The type parameter Model represents the type of data that can be searched.
    """

    def __init__(self, connection):
        self._connection = connection

    @abstractmethod
    def search(self, query_builder, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, key, **kwargs):
        raise NotImplementedError