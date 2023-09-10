from __future__ import annotations
from functools import lru_cache
from typing import Any

from .gloomhaven_exception import RestrictionException
from .achievement import Achievement
from .dict_const import DICT_CONST


class Restriction:
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
    ) -> Restriction:
        return Restriction(achievement, is_done, level)

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
            raise RestrictionException(f"Invalid requirement value: {level}")

    def to_dict(self) -> dict[str, Any]:
        return {
            DICT_CONST.IS_DONE: self.is_done,
            DICT_CONST.LEVEL: self.level,
            DICT_CONST.ACHIEVEMENT_ID: self.achievement.id,
        }
