from __future__ import annotations
import pytest
import os
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))
sys.path.append(project_root_dir)


from backend.src.gloomhaven_pckg import Coordinates, CoordinatesException


def test_create_coodrinates() -> None:
    coord = Coordinates.create("A", 5)
    assert coord.x == "A"
    assert coord.y == 5


def test_create_coordinates_by_string():
    # Test creating Coordinates from a string
    coord = Coordinates.create_by_string("B-7")
    assert coord.x == "B"
    assert coord.y == 7


def test_create_coordinates_invalid_string():
    with pytest.raises(CoordinatesException):
        Coordinates.create_by_string("Invalid-String")


def test_coordinates_out_of_bounds():
    with pytest.raises(CoordinatesException):
        Coordinates.create("Z", 5)

    with pytest.raises(CoordinatesException):
        Coordinates.create("A", 0)

    with pytest.raises(CoordinatesException):
        Coordinates.create("A", 19)

    with pytest.raises(CoordinatesException):
        Coordinates.create_by_string("A-0")

    with pytest.raises(CoordinatesException):
        Coordinates.create_by_string("A-19")


def test_get_set() -> None:
    coord = Coordinates.create("A", 5)

    coord.x = "C"
    assert coord.x == "C"
    assert coord.y == 5

    coord.y = 10
    assert coord.x == "C"
    assert coord.y == 10


def test_get_set_out_of_bounds() -> None:
    coord = Coordinates.create("A", 5)

    with pytest.raises(CoordinatesException):
        coord.x = "Z"
    assert coord.x == "A"
    assert coord.y == 5

    with pytest.raises(CoordinatesException):
        coord.y = 105
    assert coord.x == "A"
    assert coord.y == 5
