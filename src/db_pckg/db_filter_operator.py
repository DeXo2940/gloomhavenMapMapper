from __future__ import annotations

import enum


class DbFilterOperator(enum.Enum):
    EQAL = enum.auto()
    GREATER = enum.auto()
    GREATER_EQUAL = enum.auto()
    LESS_THAN = enum.auto()
    LESS_THAN_EQUAL = enum.auto()
    NOT_EQUAL = enum.auto()
    CONTAIN_PATTERN = enum.auto()
    # Needs special handling
    # in/nin : array
    IN = enum.auto()
    NOT_IN = enum.auto()
