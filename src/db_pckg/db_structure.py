from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from .db_generic_filter import DbGenericFilter


class DbStructure(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_key_value(self) -> DbGenericFilter:
        pass
