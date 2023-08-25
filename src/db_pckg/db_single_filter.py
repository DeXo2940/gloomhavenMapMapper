from __future__ import annotations
from typing import Any


from .db_exceptions import DbException
from .db_filter_operator import DbFilterOperator


class DbSingleFilter:
    def __init__(
        self, field: str, operator: DbFilterOperator, value: str | int | list[str | int]
    ) -> None:
        self.field = field
        self._operator = operator  # is public, but needs value to validate
        self.value = value

    @staticmethod
    def create(field: str, operator: DbFilterOperator, value: Any) -> DbSingleFilter:
        return DbSingleFilter(field, operator, value)

    @property
    def field(self) -> str:
        return self._field

    @field.setter
    def field(self, field: str) -> None:
        self._field = field

    @property
    def operator(self) -> DbFilterOperator:
        return self._operator

    @operator.setter
    def operator(self, operator: DbFilterOperator) -> None:
        self._operator = operator
        self._validate_operator_value()

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: str | int | list[str | int]) -> None:
        self._value = value
        self._validate_operator_value()

    def _validate_operator_value(self) -> None:
        if self._operator in [DbFilterOperator.IN, DbFilterOperator.NOT_IN]:
            if not isinstance(self._value, list):
                raise DbException(
                    f"Operator {self._operator.name} only accepts a list as a value"
                )
        else:
            if isinstance(self._value, list):
                raise DbException(
                    f"Operator {self._operator.name} only accepts single value"
                )
