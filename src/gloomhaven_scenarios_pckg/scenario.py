from __future__ import annotations
from typing import Any

from db_pckg import UniqueKeyDbStructure

from .gloomhaven_exception import ScenarioException
from .achievement_dao import AchievementDAO
from .requirement import Requirement
from .coordinates import Coordinates


class Scenario(UniqueKeyDbStructure):
    def __init__(self, id: int, coordinates: Coordinates, name: str) -> None:
        self._validate_id(id)
        super().__init__(id)
        self.coordinates = coordinates
        self.name = name
        self.blockers = []
        self.notes = ""
        # self._unlocks: list[GloomhavenScenario] = []

    @staticmethod
    def create(id: int, coordinates: Coordinates, name: str) -> Scenario:
        return Scenario(id, coordinates, name)

    @staticmethod
    def create_empty(id: int) -> Scenario:
        return Scenario(id, Coordinates.create_by_string("A-1"), f"Empty Name {id}")

    @staticmethod
    def create_from_dict(
        object_dict: dict[str, Any], composing_dao: AchievementDAO
    ) -> Scenario:
        id = object_dict.get("_id")
        if id is None:
            raise ScenarioException("Incorrect scenario Id")
        scenario_id = int(id)

        name = str(object_dict.get("name"))

        coordinates = str(object_dict.get("coords"))
        scenario_coordinates = Coordinates.create_by_string(coordinates)

        scenario = Scenario(scenario_id, scenario_coordinates, name)

        notes = object_dict.get("notes")
        if notes != None:
            scenario.notes = notes

        scenario_blockers: list[dict[str, Any]] = []
        blockers = object_dict.get("blockers")
        if blockers != None and isinstance(blockers, list):
            scenario_blockers = blockers

        for blocker in scenario_blockers:
            scenario_blocker = Requirement.create_from_dict(blocker, composing_dao)
            scenario.add_blocker(scenario_blocker)

        return scenario

    def _validate_id(self, id: int) -> None:
        if not (1 <= id <= 95):
            raise ValueError

    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, notes: str) -> None:
        self._notes = notes

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
    def blockers(self) -> list[Requirement]:
        return self._blockers

    @blockers.setter
    def blockers(self, blockers: list[Requirement]) -> None:
        self._blockers = blockers

    def add_blocker(self, blocker: Requirement) -> None:
        if blocker in self._blockers:
            raise ScenarioException("Requirement already in scenario blockers")
        self._blockers.append(blocker)

    def remove_blocker(self, blocker: Requirement) -> None:
        if blocker not in self._blockers:
            raise ScenarioException("No such requirement in scenario blockers")
        self._blockers.remove(blocker)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "_id": self._id,
            "coords": str(self._coordinates),
            "name": self._name,
            "blockers": [blocker.to_dict() for blocker in self._blockers],
            "notes": self._notes,
        }
        return result
