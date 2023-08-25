from abc import ABC, abstractmethod
from typing import Any

from .db_structure import DbStructure
from .db_filter import DbFilter


class DbAccess(ABC):
    @abstractmethod
    def find_single(self, key: DbFilter) -> dict[str, Any]:
        pass

    @abstractmethod
    def find(self, filter: DbFilter | None = None) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def update(self, object: DbStructure) -> None:
        pass

    @abstractmethod
    def update_bulk(self, objects: list[DbStructure]) -> None:
        pass

    @abstractmethod
    def delete(self, object: DbStructure) -> None:
        pass

    @abstractmethod
    def delete_bulk(self, objects: list[DbStructure]) -> None:
        pass
