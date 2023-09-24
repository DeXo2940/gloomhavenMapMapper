from __future__ import annotations
import pytest
import os
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))
sys.path.append(project_root_dir)


from backend.src.gloomhaven_pckg import AchievementType, AchievementException


TYPE = AchievementType.GLOBAL
TYPE_NAME = TYPE.name


def test_get() -> None:
    assert TYPE == AchievementType.get(TYPE_NAME)
    assert TYPE == AchievementType.get(TYPE_NAME.lower())


def test_get_incorrect():
    with pytest.raises(AchievementException):
        AchievementType.get("bad_name")


# def test_create_from_incorrect() -> None:
#     achievement_dict = {
#         DICT_CONST.ID: ID,
#         DICT_CONST.NAME: NAME,
#         DICT_CONST.TYPE: "bad type",
#     }
#     with pytest.raises(AchievementException):
#         Achievement.create_from_dict(achievement_dict)

#     achievement_dict = {DICT_CONST.ID: ID, DICT_CONST.NAME: NAME}
#     with pytest.raises(AchievementException):
#         Achievement.create_from_dict(achievement_dict)

#     achievement_dict = {DICT_CONST.ID: ID, DICT_CONST.TYPE: TYPE_NAME}
#     with pytest.raises(AchievementException):
#         Achievement.create_from_dict(achievement_dict)


# def test_create_empty() -> None:
#     achievement = Achievement.create_empty(ID)
#     assert achievement.id == ID


# def test_get_set() -> None:
#     CHANGED_NAME = "Changed name"

#     achievement = Achievement.create(NAME, TYPE, ID)

#     with pytest.raises(AttributeError):
#         achievement.id = 5  # type: ignore

#     achievement.name = CHANGED_NAME
#     achievement.type = AchievementType.TEAM

#     assert achievement.id == ID
#     assert achievement.name == CHANGED_NAME
#     assert achievement.type == AchievementType.TEAM


# def test_to_dict():
#     achievement = Achievement.create(NAME, TYPE, ID)

#     achievement_dict = achievement.to_dict()

#     assert achievement_dict.get(DICT_CONST.ID) == ID
#     assert achievement_dict.get(DICT_CONST.NAME) == NAME
#     assert achievement_dict.get(DICT_CONST.TYPE) == TYPE_NAME