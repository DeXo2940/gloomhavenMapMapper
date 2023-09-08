from __future__ import annotations
from functools import lru_cache
from .gloomhaven_exception import CoordinatesException


class Coordinates:
    def __init__(self, x: str, y: int) -> None:
        self.x = x
        self.y = y

    @lru_cache(maxsize=None)
    @staticmethod
    def create(x: str, y: int) -> Coordinates:
        return Coordinates(x, y)

    @lru_cache(maxsize=None)
    @staticmethod
    def create_by_string(coordinates: str) -> Coordinates:
        splited: list[str] = coordinates.split("-")
        if len(splited) != 2:
            raise CoordinatesException(f"Incorrect coordinates format: {coordinates}")
        try:
            return Coordinates(splited[0], int(splited[1]))
        except ValueError:
            raise CoordinatesException(f"Incorrect coordinates value: {coordinates}")

    @property
    def x(self) -> str:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @x.setter
    def x(self, x: str) -> None:
        self._validate_x(x)
        self._x = x.upper()

    @y.setter
    def y(self, y: int) -> None:
        self._validate_y(y)
        self._y = y

    def _validate_x(self, x: str) -> None:
        x = x.upper()
        if not (len(x) == 1 and "A" <= x <= "O"):
            raise CoordinatesException(f"x ={x} - Coordinate out of bounds")

    def _validate_y(self, y: int) -> None:
        if not (1 <= y <= 18):
            raise CoordinatesException(f"y ={y} - Coordinate out of bounds")

    def __str__(self) -> str:
        return f"{self.x}-{self.y}"
