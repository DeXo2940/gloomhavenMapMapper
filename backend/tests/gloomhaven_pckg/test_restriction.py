from __future__ import annotations
import pytest
import mock
import os
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))
sys.path.append(project_root_dir)


from backend.src.gloomhaven_pckg import (
    Achievement,
    Restriction,
    RestrictionException,
    DICT_CONST,
)


# NAME = "Test name"
# TYPE = AchievementType.GLOBAL
# TYPE_NAME = TYPE.name
# ID = 156


def test_create_restriction() -> None:
    achievement_mock = mock.Mock(spec=Achievement)
    restriction = Restriction.create(achievement_mock, True, 3)

    assert restriction.achievement == achievement_mock
    assert restriction.is_done == True
    assert restriction.level == 3


def test_create_restriction_no_level() -> None:
    achievement_mock = mock.Mock(spec=Achievement)
    restriction = Restriction.create(achievement_mock, False)

    assert restriction.achievement == achievement_mock
    assert restriction.is_done == False
    assert restriction.level is None


def test_get_set():
    achievement_mock_1 = mock.Mock(spec=Achievement)
    achievement_mock_2 = mock.Mock(spec=Achievement)

    restriction = Restriction.create(achievement_mock_1, False)

    restriction.achievement = achievement_mock_2
    restriction.is_done = True
    restriction.level = 2

    assert restriction.achievement == achievement_mock_2
    assert restriction.is_done == True
    assert restriction.level == 2

    restriction.level = None
    assert restriction.level is None


def test_level_out_of_bounds():
    achievement_mock = mock.Mock(spec=Achievement)
    restriction = Restriction.create(achievement_mock, False)

    with pytest.raises(RestrictionException):
        Restriction.create(achievement_mock, False, 0)
    with pytest.raises(RestrictionException):
        Restriction.create(achievement_mock, False, 6)
    with pytest.raises(RestrictionException):
        restriction.level = 16
    with pytest.raises(RestrictionException):
        restriction.level = 0


def test_to_dict() -> None:
    ID = 166

    achievement_mock = mock.Mock(spec=Achievement)
    achievement_mock.id = ID

    restriction = Restriction.create(achievement_mock, False)

    restriction_dict = restriction.to_dict()
    assert restriction_dict.get(DICT_CONST.ACHIEVEMENT_ID) == ID
    assert restriction_dict.get(DICT_CONST.LEVEL) is None
    assert restriction_dict.get(DICT_CONST.IS_DONE) == False
