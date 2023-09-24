from __future__ import annotations
import random
from re import L
import string
import pytest
import peewee
import mock
import os
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))
sys.path.append(project_root_dir)

from backend.src.gloomhaven_pckg import (
    Achievement,
    AchievementType,
    DICT_CONST,
    AchievementException,
    AchievementRepository,
)

from backend.src.gloomhaven_model_pckg import database_proxy, MODELS

NAME = "Test name"
TYPE = AchievementType.GLOBAL
TYPE_NAME = TYPE.name
ID = 156


def test_get_instance_achievement_repository():
    achievement_repository_1 = AchievementRepository.get_instance()
    achievement_repository_2 = AchievementRepository.get_instance()

    assert achievement_repository_1 == achievement_repository_2


def test_create() -> None:
    achievement_mock = build_achievement_mock()
    achievement_mock.id = None
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()
    achievement = achievement_repository.create(achievement_mock)

    assert achievement.id is not None
    assert achievement.name == NAME
    assert achievement.type == TYPE

    achievement_mock.id = ID
    achievement = achievement_repository.create(achievement_mock)

    assert achievement.id == ID
    assert achievement.name == NAME
    assert achievement.type == TYPE

    with pytest.raises(AchievementException):
        achievement_repository.create(achievement_mock)


def test_read() -> None:
    NUMBER_OF_RECORDS = 10
    achievement_mock = build_achievement_mock()
    achievement_mock.id = None
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()

    achievements = achievement_repository.read()
    assert achievements == []

    for _ in range(NUMBER_OF_RECORDS):
        achievement_repository.create(achievement_mock)

    achievements = achievement_repository.read()
    assert len(achievements) == NUMBER_OF_RECORDS


def test_read_by_partial_name() -> None:
    NUMBER_OF_RECORDS = 10
    PART_NAME = "sth"
    achievement_mock = build_achievement_mock()
    achievement_mock.id = None
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()

    achievements = achievement_repository.read_by_partial_name(PART_NAME)
    assert achievements == []

    generate_random_records(achievement_repository)
    for _ in range(NUMBER_OF_RECORDS):
        achievement_mock.name = (
            "".join(random.choices(string.ascii_lowercase, k=5))
            + PART_NAME
            + "".join(random.choices(string.ascii_lowercase, k=5))
        )

        achievement_repository.create(achievement_mock)
    generate_random_records(achievement_repository)

    achievements = achievement_repository.read_by_partial_name(PART_NAME)
    assert len(achievements) == NUMBER_OF_RECORDS


def test_read_by_id() -> None:
    achievement_mock = build_achievement_mock()
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()

    with pytest.raises(AchievementException):
        achievement_repository.read_by_id(ID)

    generate_random_records(achievement_repository)
    achievement = achievement_repository.create(achievement_mock)
    generate_random_records(achievement_repository)

    found_achievement = achievement_repository.read_by_id(ID)
    compare_achievements(found_achievement, achievement)


def test_read_by_name() -> None:
    achievement_mock = build_achievement_mock()
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()

    with pytest.raises(AchievementException):
        achievement_repository.read_by_name(NAME)

    generate_random_records(achievement_repository)
    achievement = achievement_repository.create(achievement_mock)
    generate_random_records(achievement_repository)

    found_achievement = achievement_repository.read_by_name(NAME)
    compare_achievements(found_achievement, achievement)


def test_update():
    achievement_mock = build_achievement_mock()
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()

    with pytest.raises(AchievementException):
        achievement_repository.update(achievement_mock)

    generate_random_records(achievement_repository)
    achievement = achievement_repository.create(achievement_mock)
    generate_random_records(achievement_repository)

    achievement.name = "Changed name"
    achievement_repository.update(achievement)

    found_achievement = achievement_repository.read_by_id(ID)
    compare_achievements(found_achievement, achievement)


def test_delete() -> None:
    achievement_mock = build_achievement_mock()
    initialize_db()

    achievement_repository = AchievementRepository.get_instance()

    generate_random_records(achievement_repository)
    achievement = achievement_repository.create(achievement_mock)
    generate_random_records(achievement_repository)

    achievement_repository.delete(achievement_mock)

    with pytest.raises(AchievementException):
        achievement_repository.read_by_id(ID)


def initialize_db() -> None:
    database = peewee.SqliteDatabase(":memory:")
    database_proxy.initialize(database)

    database_proxy.create_tables(MODELS, safe=True)


def generate_random_records(achievement_repository: AchievementRepository) -> None:
    achievement_mock_any = build_achievement_mock()
    achievement_mock_any.id = None
    achievement_mock_any.name = "Bad name"
    achievement_mock_any.type = TYPE

    for _ in range(random.randint(0, 10)):
        achievement_repository.create(achievement_mock_any)


def build_achievement_mock() -> mock.Mock:
    achievement_mock = mock.Mock(spec=Achievement)
    achievement_mock.id = ID
    achievement_mock.name = NAME
    achievement_mock.type = TYPE
    return achievement_mock


def compare_achievements(current: Achievement, expected: Achievement) -> None:
    assert current.id == expected.id
    assert current.name == expected.name
    assert current.type == expected.type
