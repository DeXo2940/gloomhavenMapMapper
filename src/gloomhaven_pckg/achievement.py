from __future__ import annotations
from functools import lru_cache

from .achievement_type import AchievementType


class Achievement:
    def __init__(
        self,
        id: int | None,
        name: str,
        type: AchievementType,
    ) -> None:
        self._id = id
        self.name = name
        self.type = type

    @staticmethod
    @lru_cache(maxsize=None)
    def create(name: str, type: AchievementType, id: int | None = None) -> Achievement:
        return Achievement(id, name, type)

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    @property
    def type(self) -> AchievementType:
        return self._type

    @type.setter
    def type(self, type: AchievementType) -> None:
        self._type = type
