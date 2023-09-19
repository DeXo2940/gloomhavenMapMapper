from __future__ import annotations
import enum

from .gloomhaven_exception import AchievementException


class AchievementType(enum.Enum):
    GLOBAL = enum.auto()
    TEAM = enum.auto()

    @staticmethod
    def get(name: str) -> AchievementType:
        try:
            return AchievementType[name.upper()]
        except KeyError:
            raise AchievementException(f"Incorrect Achievement Type: {name}")
