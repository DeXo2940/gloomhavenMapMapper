from __future__ import annotations
from functools import lru_cache
from typing import Any

# from .achievement_dao import AchievementDAO
from .gloomhaven_exception import RequirementException
from .achievement import Achievement


class Requirement:
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
    ) -> Requirement:
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
