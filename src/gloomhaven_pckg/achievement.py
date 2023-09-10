from __future__ import annotations
from functools import lru_cache
from typing import Any

from gloomhaven_pckg.gloomhaven_exception import AchievementException

from .achievement_type import AchievementType
from .dict_const import DICT_CONST


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

    @staticmethod
    def create_from_dict(achievement_dict: dict[str, Any]) -> Achievement:
        id = achievement_dict.get(DICT_CONST.ID)
        name = achievement_dict.get(DICT_CONST.NAME)
        type_name = achievement_dict.get(DICT_CONST.TYPE)
        if name is None or type_name is None:
            raise AchievementException("Incorrect values for Achievement creation")
        achievement_type = AchievementType[type_name]
        return Achievement.create(name, achievement_type, id)

    @staticmethod
    def create_empty(id: int) -> Achievement:
        return Achievement.create("Empty Name", AchievementType.GLOBAL, id)

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

    def to_dict(self) -> dict[str, Any]:
        return {
            DICT_CONST.ID: self.id,
            DICT_CONST.NAME: self.name,
            DICT_CONST.TYPE: self.type.name,
        }
