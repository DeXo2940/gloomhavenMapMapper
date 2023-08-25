from __future__ import annotations
from typing import Any

from .db_exceptions import DbException
from .db_single_filter import DbSingleFilter
from .db_filter import DbFilter
from .db_filter_operator import DbFilterOperator
from .db_generic_filter import DbGenericFilter


class MognoDbFilter(DbFilter):
    OPERATION_TRANSLATION = {
        DbFilterOperator.EQAL: "$eq",
        DbFilterOperator.GREATER: "$gt",
        DbFilterOperator.GREATER_EQUAL: "$gte",
        DbFilterOperator.LESS_THAN: "$lt",
        DbFilterOperator.LESS_THAN_EQUAL: "$lte",
        DbFilterOperator.NOT_EQUAL: "$ne",
        DbFilterOperator.CONTAIN_PATTERN: "$regex",
        DbFilterOperator.IN: "$in",
        DbFilterOperator.NOT_IN: "$nin",
    }

    @staticmethod
    def create(filters: list[DbSingleFilter] = []) -> MognoDbFilter:
        return MognoDbFilter(filters)

    @staticmethod
    def create_by_generic(db_generic_filter: DbGenericFilter) -> MognoDbFilter:
        filters = db_generic_filter.filters
        return MognoDbFilter(filters)

    def translate_for_db(self) -> dict[str, dict[str, Any]]:
        db_dictionary: dict[str, dict[str, Any]] = {}

        unique_filter_fields = self._get_unique_filter_fields()

        while len(unique_filter_fields) != 0:
            current_filter_field = unique_filter_fields.pop(0)
            same_field_filters = self._get_same_field_filters(current_filter_field)
            operators_values = self._get_operator_values(same_field_filters)

            db_dictionary[current_filter_field] = operators_values

        return db_dictionary

    def _get_unique_filter_fields(self) -> list[str]:
        return list(set([filter.field for filter in self._filters]))

    def _get_same_field_filters(self, field: str) -> list[DbSingleFilter]:
        return [filter for filter in self._filters if filter.field == field]

    def _get_operator_values(
        self, same_field_filters: list[DbSingleFilter]
    ) -> dict[str, Any]:
        operators_values: dict[str, Any] = {}
        for filter in same_field_filters:
            translated_operator = self._translate_filter_operator(filter.operator)
            operators_values[translated_operator] = filter.value
            if filter.operator == DbFilterOperator.CONTAIN_PATTERN:
                operators_values = self._add_ignore_case_for_regex(operators_values)
        return operators_values

    def _translate_filter_operator(self, operator: DbFilterOperator) -> str:
        if operator not in MognoDbFilter.OPERATION_TRANSLATION:
            raise DbException(f"Operator {operator.name} is undefined")
        return MognoDbFilter.OPERATION_TRANSLATION[operator]

    def _add_ignore_case_for_regex(
        self, operators_values: dict[str, Any]
    ) -> dict[str, Any]:
        operators_values["$options"] = "i"
        return operators_values
