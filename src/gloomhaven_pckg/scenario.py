from __future__ import annotations
from typing import Any


from .gloomhaven_exception import ScenarioException
from .restriction import Restriction
from .coordinates import Coordinates
from .achievement import Achievement
from .achievement_repository import AchievementRepository
from .dict_const import DICT_CONST


class Scenario:
    def __init__(self, id: int, coordinates: Coordinates, name: str) -> None:
        self._validate_id(id)
        self._id = id
        self.coordinates = coordinates
        self.name = name
        self.restrictions = []

    @staticmethod
    def create(id: int, coordinates: Coordinates, name: str) -> Scenario:
        return Scenario(id, coordinates, name)

    @staticmethod
    def create_from_dict(
        scenario_dict: dict[str, Any],
        achievement_repository: AchievementRepository | None = None,
    ) -> Scenario:
        scenario = Scenario._create_scenario_from_dict(scenario_dict)
        restriction_dicts = scenario_dict.get(DICT_CONST.RESTRICTIONS)
        restrictions = Scenario._create_restrictions_from_dicts(
            restriction_dicts, achievement_repository
        )
        scenario.restrictions = restrictions

        return scenario

    @property
    def id(self) -> int:
        return self._id

    @property
    def coordinates(self) -> Coordinates:
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates: Coordinates) -> None:
        self._coordinates = coordinates

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def restrictions(self) -> list[Restriction]:
        return self._blockers

    @restrictions.setter
    def restrictions(self, blockers: list[Restriction]) -> None:
        self._blockers = blockers

    def add_blocker(self, blocker: Restriction) -> None:
        if blocker in self._blockers:
            raise ScenarioException("Requirement already in scenario blockers")
        self._blockers.append(blocker)

    def remove_blocker(self, blocker: Restriction) -> None:
        if blocker not in self._blockers:
            raise ScenarioException("No such requirement in scenario blockers")
        self._blockers.remove(blocker)

    def to_dict(self) -> dict[str, Any]:
        return {
            DICT_CONST.ID: self.id,
            DICT_CONST.NAME: self.name,
            DICT_CONST.COORDINATES: str(self.coordinates),
            DICT_CONST.RESTRICTIONS: [
                restriction.to_dict() for restriction in self.restrictions
            ],
        }

    @staticmethod
    def _create_scenario_from_dict(scenario_dict: dict[str, Any]) -> "Scenario":
        id = scenario_dict.get(DICT_CONST.ID)
        name = scenario_dict.get(DICT_CONST.NAME)
        coordinates = scenario_dict.get(DICT_CONST.COORDINATES)
        if id is None or name is None or coordinates is None:
            raise ScenarioException("Incorrect values for Scenario creation")
        scenario_coordinates = Coordinates.create_by_string(coordinates)
        return Scenario.create(id, scenario_coordinates, name)

    @staticmethod
    def _create_restrictions_from_dicts(
        restriction_dicts: list[dict[str, Any]] | None,
        achievement_repository: AchievementRepository | None = None,
    ) -> list[Restriction]:
        restrictions = []
        if restriction_dicts is None:
            return restrictions

        for restriction_dict in restriction_dicts:
            restriction = Scenario._create_restriction_from_dict(
                restriction_dict, achievement_repository
            )
            restrictions.append(restriction)
        return restrictions

    @staticmethod
    def _create_restriction_from_dict(
        restriction_dict: dict[str, Any],
        achievement_repository: AchievementRepository | None = None,
    ) -> Restriction:
        achievement_id = restriction_dict.get(DICT_CONST.ACHIEVEMENT_ID)
        is_done = restriction_dict.get(DICT_CONST.IS_DONE)
        level = restriction_dict.get(DICT_CONST.LEVEL)
        if achievement_id is None or is_done is None:
            raise ScenarioException(
                "Incorrect values for Scenario Restriction creation"
            )
        achievement = (
            Achievement.create_empty(achievement_id)
            if achievement_repository is None
            else achievement_repository.read_by_id(achievement_id)
        )
        return Restriction.create(achievement, is_done, level)

    def _validate_id(self, id: int) -> None:
        if not (1 <= id <= 95):
            raise ScenarioException(f"id = `{id}` is outside of permited range")
