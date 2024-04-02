from abc import ABC
from typing import Generic

from src.core.types import Model

class Repository(ABC, Generic[Model]):
    """The Repository class defines an abstract
    interface for interacting with a data store.
    It provides a way to separate the data access
    logic from the business logic of an application,
    which helps to improve maintainability and scalability.

    The Repository class is generic, allowing
    it to be used with different types of data models.
    The type parameter Model represents the type of
    data that will be stored in the repository."""

    def __init__(self, connection) -> None:
        self._connection = connection

    def get(self, key) -> Model:
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError
