from __future__ import annotations


from .db_exceptions import DbException
from .db_single_filter import DbSingleFilter


class DbGenericFilter:
    def __init__(self, filters: list[DbSingleFilter] = []) -> None:
        self._filters = filters

    @staticmethod
    def create(filters: list[DbSingleFilter] = []) -> DbGenericFilter:
        return DbGenericFilter(filters)

    @property
    def filters(self) -> list[DbSingleFilter]:
        return self._filters

    def add_filter(self, filter: DbSingleFilter) -> None:
        if filter in self._filters:
            raise DbException("Filter already exists")
        self._filters.append(filter)

    def remove_filter(self, filter: DbSingleFilter) -> None:
        if filter not in self._filters:
            raise DbException("No such filter exists")
        self._filters.remove(filter)

    def remove_all_filters(self) -> None:
        self._filters = []
