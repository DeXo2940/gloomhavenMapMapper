from __future__ import annotations
import pytest
import mock
import os
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))
sys.path.append(project_root_dir)

from backend.src.gloomhaven_pckg import (
    Scenario,
    ScenarioException,
    Restriction,
    DICT_CONST,
    Coordinates,
)


# TYPE = AchievementType.GLOBAL
# TYPE_NAME = TYPE.name
ID = 32
ACHIEVEMENT_ID = 152
NAME = "Test name"


def test_create_scenario() -> None:
    coordinates_mock = mock.Mock(spec=Coordinates)
    scenario = Scenario.create(ID, coordinates_mock, NAME)

    assert scenario.id == ID
    assert scenario.name == NAME
    assert scenario.coordinates == coordinates_mock
    assert scenario.restrictions == []


def test_create_scenario_from_dict() -> None:
    COORDINATES_STRING = "A-1"

    restriction_mock = mock.Mock(spec=Restriction)
    restriction_mock.to_dict.return_value = {
        DICT_CONST.IS_DONE: True,
        DICT_CONST.LEVEL: None,
        DICT_CONST.ACHIEVEMENT_ID: ACHIEVEMENT_ID,
    }

    scenario_dict = {
        DICT_CONST.ID: ID,
        DICT_CONST.NAME: NAME,
        DICT_CONST.COORDINATES: COORDINATES_STRING,
        DICT_CONST.RESTRICTIONS: [restriction_mock.to_dict()],
    }
    scenario = Scenario.create_from_dict(scenario_dict)

    assert scenario.id == ID
    assert scenario.name == NAME
    assert str(scenario.coordinates) == COORDINATES_STRING
    assert len(scenario.restrictions) == 1
    restriction = scenario.restrictions[0]
    assert restriction.to_dict() == restriction_mock.to_dict()


def test_id_out_of_bounds():
    coordinates_mock = mock.Mock(spec=Coordinates)

    with pytest.raises(ScenarioException):
        Scenario.create(0, coordinates_mock, NAME)
    with pytest.raises(ScenarioException):
        Scenario.create(96, coordinates_mock, NAME)


def test_get_set() -> None:
    CHANGED_NAME = "New Name"
    coordinates_mock_1 = mock.Mock(spec=Coordinates)
    coordinates_mock_2 = mock.Mock(spec=Coordinates)
    restriction_mock_1 = mock.Mock(spec=Restriction)
    restriction_mock_2 = mock.Mock(spec=Restriction)
    scenario = Scenario.create(ID, coordinates_mock_1, NAME)

    with pytest.raises(AttributeError):
        scenario.id = 5  # type: ignore

    scenario.name = CHANGED_NAME
    scenario.coordinates = coordinates_mock_2
    scenario.restrictions = [restriction_mock_1, restriction_mock_2]

    assert scenario.name == CHANGED_NAME
    assert scenario.coordinates == coordinates_mock_2
    assert scenario.restrictions == [restriction_mock_1, restriction_mock_2]

    scenario.restrictions = [restriction_mock_2]
    assert scenario.restrictions == [restriction_mock_2]

    scenario.restrictions = []
    assert scenario.restrictions == []


def test_add_restriction() -> None:
    coordinates_mock = mock.Mock(spec=Coordinates)
    restriction_mock_1 = mock.Mock(spec=Restriction)
    restriction_mock_2 = mock.Mock(spec=Restriction)

    scenario = Scenario.create(ID, coordinates_mock, NAME)

    scenario.add_restriction(restriction_mock_1)

    assert len(scenario.restrictions) == 1
    assert scenario.restrictions[0] == restriction_mock_1

    scenario.add_restriction(restriction_mock_2)

    assert len(scenario.restrictions) == 2

    with pytest.raises(ScenarioException):
        scenario.add_restriction(restriction_mock_1)
    with pytest.raises(ScenarioException):
        scenario.add_restriction(restriction_mock_2)

    assert len(scenario.restrictions) == 2


def test_remove_restriction():
    coordinates_mock = mock.Mock(spec=Coordinates)
    restriction_mock_1 = mock.Mock(spec=Restriction)
    restriction_mock_2 = mock.Mock(spec=Restriction)

    scenario = Scenario.create(ID, coordinates_mock, NAME)

    scenario.restrictions = [restriction_mock_1, restriction_mock_2]

    scenario.remove_restriction(restriction_mock_2)
    assert len(scenario.restrictions) == 1
    assert scenario.restrictions[0] == restriction_mock_1

    with pytest.raises(ScenarioException):
        scenario.remove_restriction(restriction_mock_2)

    scenario.remove_restriction(restriction_mock_1)
    assert scenario.restrictions == []


#     achievement_mock_1 = mock.Mock(spec=Achievement)
#     achievement_mock_2 = mock.Mock(spec=Achievement)

#     restriction = Restriction.create(achievement_mock_1, False)

#     restriction.achievement = achievement_mock_2
#     restriction.is_done = True
#     restriction.level = 2

#     assert restriction.achievement == achievement_mock_2
#     assert restriction.is_done == True
#     assert restriction.level == 2

#     restriction.level = None
#     assert restriction.level is None


# def test_level_out_of_bounds():
#     achievement_mock = mock.Mock(spec=Achievement)
#     restriction = Restriction.create(achievement_mock, False)

#     with pytest.raises(RestrictionException):
#         Restriction.create(achievement_mock, False, 0)
#     with pytest.raises(RestrictionException):
#         Restriction.create(achievement_mock, False, 6)
#     with pytest.raises(RestrictionException):
#         restriction.level = 16
#     with pytest.raises(RestrictionException):
#         restriction.level = 0


# def test_to_dict() -> None:
#     ID = 166

#     achievement_mock = mock.Mock(spec=Achievement)
#     achievement_mock.id = ID

#     restriction = Restriction.create(achievement_mock, False)

#     restriction_dict = restriction.to_dict()
#     assert restriction_dict.get(DICT_CONST.ACHIEVEMENT_ID) == ID
#     assert restriction_dict.get(DICT_CONST.LEVEL) is None
#     assert restriction_dict.get(DICT_CONST.IS_DONE) == False
