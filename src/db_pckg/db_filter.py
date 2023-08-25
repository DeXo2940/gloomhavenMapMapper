from __future__ import annotations
from abc import abstractmethod
from typing import Any

from .db_generic_filter import DbGenericFilter


class DbFilter(DbGenericFilter):
    @abstractmethod
    def translate_for_db(self) -> dict[str, dict[str, Any]]:
        pass
