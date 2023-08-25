from __future__ import annotations
from functools import lru_cache
import itertools
from typing import Any

from db_pckg import UniqueKeyDbStructure

from .achievement_type import AchievementType


class Achievement(UniqueKeyDbStructure):
    id_iter = itertools.count()

    def __init__(
        self,
        name: str,
        type: AchievementType,
        id: int | None = None,
    ) -> None:
        if id == None:
            id = next(self.id_iter)
        super().__init__(id)
        self.name = name
        self.type = type

    @staticmethod
    @lru_cache(maxsize=None)
    def create(name: str, type: AchievementType) -> Achievement:
        return Achievement(name, type)

    @staticmethod
    def create_from_dict(object_dict: dict[str, Any]) -> Achievement:  # DBStructure
        id = object_dict["_id"]
        name = object_dict["name"]
        type_name = object_dict["type"]
        type = AchievementType[type_name]

        return Achievement(name, type, id)

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
            "_id": self._id,
            "name": self._name,
            "type": self._type.name,
        }
