from __future__ import annotations
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any

from .db_filter_operator import DbFilterOperator
from .db_single_filter import DbSingleFilter
from .db_structure import DbStructure
from .db_filter import DbFilter
from .db_generic_filter import DbGenericFilter


class UniqueKeyDbStructure(DbStructure):
    def __init__(self, id: int) -> None:
        self._id = id

    @property
    def id(self) -> int:
        return self._id

    @lru_cache(maxsize=1)
    def get_key_value(self) -> DbGenericFilter:
        single_filter = DbSingleFilter.create("_id", DbFilterOperator.EQAL, self.id)
        return DbGenericFilter.create([single_filter])

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass
