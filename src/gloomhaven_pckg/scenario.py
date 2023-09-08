from __future__ import annotations

from .gloomhaven_exception import ScenarioException
from .requirement import Requirement
from .coordinates import Coordinates


class Scenario:
    def __init__(self, id: int, coordinates: Coordinates, name: str) -> None:
        self._validate_id(id)
        self._id = id
        self.coordinates = coordinates
        self.name = name
        self.blockers = []
        self.notes = ""

    @staticmethod
    def create(id: int, coordinates: Coordinates, name: str) -> Scenario:
        return Scenario(id, coordinates, name)

    @staticmethod
    def create_empty(id: int) -> Scenario:
        return Scenario(id, Coordinates.create_by_string("A-1"), f"Empty Name {id}")

    def _validate_id(self, id: int) -> None:
        if not (1 <= id <= 95):
            raise ValueError

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
    def blockers(self) -> list[Requirement]:
        return self._blockers

    @blockers.setter
    def blockers(self, blockers: list[Requirement]) -> None:
        self._blockers = blockers

    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, notes: str) -> None:
        self._notes = notes

    def add_blocker(self, blocker: Requirement) -> None:
        if blocker in self._blockers:
            raise ScenarioException("Requirement already in scenario blockers")
        self._blockers.append(blocker)

    def remove_blocker(self, blocker: Requirement) -> None:
        if blocker not in self._blockers:
            raise ScenarioException("No such requirement in scenario blockers")
        self._blockers.remove(blocker)
