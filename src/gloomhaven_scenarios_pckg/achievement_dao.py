from __future__ import annotations
from functools import lru_cache

from db_pckg import (
    DbAccess,
    MognoDbFilter,
    DbSingleFilter,
    DbFilterOperator,
    DbStructure,
)

from .achievement import Achievement


class AchievementDAO:
    COLLECTION_NAME = "achievements"

    def __init__(self, db_access: DbAccess) -> None:
        self._db_access: DbAccess = db_access

    @lru_cache(maxsize=1)
    @staticmethod
    def get_instance(db_access: DbAccess) -> AchievementDAO:
        return AchievementDAO(db_access)

    def find_by_id(self, id: int) -> Achievement:
        db_single_filter = DbSingleFilter("_id", DbFilterOperator.EQAL, id)
        key_filter = MognoDbFilter([db_single_filter])

        db_dict = self._db_access.find_single(key_filter)
        return Achievement.create_from_dict(db_dict)

    def find_all(self) -> list[Achievement]:
        achievements: list[Achievement] = []
        db_dicts = self._db_access.find()
        for db_dict in db_dicts:
            achievement = Achievement.create_from_dict(db_dict)
            achievements.append(achievement)
        return achievements

    def save_one(self, achievement: Achievement) -> None:
        self._db_access.update(achievement)

    def save_many(self, achievements: list[Achievement]) -> None:
        db_structures = self._translate_achievements_to_dbstructures(achievements)
        self._db_access.update_bulk(db_structures)

    def _translate_achievements_to_dbstructures(self, achievements: list[Achievement]):
        # for some reason when Achievement is in list the IDE shows a type error
        db_structures: list[DbStructure] = []
        for achievement in achievements:
            db_structures.append(achievement)
        return db_structures
