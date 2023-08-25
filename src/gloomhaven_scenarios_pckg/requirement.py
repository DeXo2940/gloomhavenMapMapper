from __future__ import annotations
from functools import lru_cache
from typing import Any

from db_pckg import DbStructure, DbSingleFilter, DbGenericFilter, DbFilterOperator

from .achievement_dao import AchievementDAO
from .gloomhaven_exception import RequirementException
from .achievement import Achievement


class Requirement(DbStructure):
    def __init__(
        self,
        achievement: Achievement,
        is_done: bool,
        level: int | None = None,
    ) -> None:
        self.achievement = achievement
        self.is_done = is_done
        self.level = level

    @staticmethod
    @lru_cache(maxsize=None)
    def create(
        achievement: Achievement, is_done: bool, level: int | None = None
    ) -> "Requirement":
        return Requirement(achievement, is_done, level)

    @staticmethod
    def create_from_dict(
        object_dict: dict[str, Any], composing_dao: AchievementDAO
    ) -> Requirement:
        is_done = bool(object_dict.get("is_done"))
        level = object_dict.get("level")

        achievement_id = object_dict.get("achievement")
        if achievement_id is None:
            raise RequirementException("Incorrect achievement Id")
        achievement_id = int(achievement_id)

        # TODO FIX THIS SHIT - I Need the DAO...
        achievement = composing_dao.get_by_id(achievement_id)
        if achievement is None:
            raise RequirementException(
                f"Couldn't find an achievement with id: {achievement_id}"
            )
        return Requirement(achievement, is_done, level)

    @property
    def is_done(self) -> bool:
        return self._is_done

    @is_done.setter
    def is_done(self, is_done: bool) -> None:
        self._is_done = is_done

    @property
    def achievement(self) -> Achievement:
        return self._achievement

    @achievement.setter
    def achievement(self, achievement: Achievement) -> None:
        self._achievement = achievement

    @property
    def level(self) -> int | None:
        return self._level

    @level.setter
    def level(self, level: int | None) -> None:
        self._validate_level(level)
        self._level = level

    def _validate_level(self, level) -> None:
        if not (level == None or 1 <= level <= 5):
            raise RequirementException(f"Invalid requirement value: {level}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "achievement": self._achievement.id,
            "is_done": self._is_done,
            "level": self._level,
        }

    def get_key_value(self) -> DbGenericFilter:
        generic_filter = DbGenericFilter.create()

        single_filter = self._create_single_filter("achievement", self._achievement.id)
        generic_filter.add_filter(single_filter)
        single_filter = self._create_single_filter("is_done", self._is_done)
        generic_filter.add_filter(single_filter)
        single_filter = self._create_single_filter("level", self._level)
        generic_filter.add_filter(single_filter)

        return generic_filter

    def _create_single_filter(self, key: str, value: str | int | None):
        return DbSingleFilter.create(key, DbFilterOperator.EQAL, value)
