from __future__ import annotations
from functools import lru_cache

import pickle

from db_pckg import (
    DbAccess,
    MognoDbFilter,
    DbSingleFilter,
    DbFilterOperator,
    DbStructure,
)
from gloomhaven_scenarios_pckg.achievement import Achievement
from .achievement_dao import AchievementDAO
from .requirement import Requirement
from .scenario import Scenario


class ScenarioDAO:
    COLLECTION_NAME = "scenarios"

    def __init__(self, db_access: DbAccess, achievement_dao: AchievementDAO) -> None:
        self._db_access: DbAccess = db_access
        self._achievement_dao: AchievementDAO = achievement_dao

    @lru_cache(maxsize=1)
    @staticmethod
    def get_instance(
        db_access: DbAccess, achievement_dao: AchievementDAO
    ) -> ScenarioDAO:
        return ScenarioDAO(db_access, achievement_dao)

    def find_by_id(self, id: int) -> Scenario:
        db_single_filter = DbSingleFilter("_id", DbFilterOperator.EQAL, id)
        key_filter = MognoDbFilter([db_single_filter])

        db_dict = self._db_access.find_single(key_filter)
        return Scenario.create_from_dict(db_dict, self._achievement_dao)

    def find_all(self) -> list[Scenario]:
        scenarios: list[Scenario] = []
        db_dicts = self._db_access.find()
        for db_dict in db_dicts:
            scenario = Scenario.create_from_dict(db_dict, self._achievement_dao)
            scenarios.append(scenario)
        return scenarios

    def save_one(self, scenario: Scenario) -> None:
        self._db_access.update(scenario)

    def save_many(self, scenarios: list[Scenario]) -> None:
        db_structures = self._translate_scenarios_to_dbstructures(scenarios)
        self._db_access.update_bulk(db_structures)

    def _translate_scenarios_to_dbstructures(self, scenarios: list[Scenario]):
        # for some reason when Scenario is in list the IDE shows a type error
        db_structures: list[DbStructure] = []
        for scenario in scenarios:
            db_structures.append(scenario)
        return db_structures
