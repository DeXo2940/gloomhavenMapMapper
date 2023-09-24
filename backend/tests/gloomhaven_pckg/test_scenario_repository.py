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
    Scenario,
    ScenarioRepository,
    ScenarioException,
    Coordinates,
)

from backend.src.gloomhaven_model_pckg import database_proxy, MODELS

ID = 10
NAME = "Test name"
RANDOM_GENERATOR_MAX_RANGE = 10
COORDINATES_STR = "A-1"


def test_get_instance_achievement_repository() -> None:
    scenario_repository_1 = ScenarioRepository.get_instance()
    scenario_repository_2 = ScenarioRepository.get_instance()

    assert scenario_repository_1 == scenario_repository_2


def test_create() -> None:
    scenario_mock = build_scenario_mock()

    initialize_db()
    scenario_repository = ScenarioRepository.get_instance()
    scenario = scenario_repository.create(scenario_mock)

    assert scenario.id == scenario_mock.id == ID
    assert scenario.name == scenario_mock.name == NAME
    assert (
        str(scenario.coordinates) == str(scenario_mock.coordinates) == COORDINATES_STR
    )
    assert scenario.restrictions == scenario_mock.restrictions == []

    with pytest.raises(ScenarioException):
        scenario_repository.create(scenario_mock)


def test_read() -> None:
    NUMBER_OF_RECORDS = 10
    scenario_mock = build_scenario_mock()
    initialize_db()
    scenario_repository = ScenarioRepository.get_instance()

    scenarios = scenario_repository.read()
    assert scenarios == []

    for i in range(NUMBER_OF_RECORDS):
        scenario_mock.id = i + 1
        scenario_repository.create(scenario_mock)

    scenarios = scenario_repository.read()
    assert len(scenarios) == NUMBER_OF_RECORDS


def test_read_by_partial_name() -> None:
    NUMBER_OF_RECORDS = 10
    PART_NAME = "sth"
    scenario_mock = build_scenario_mock()
    initialize_db()
    scenario_repository = ScenarioRepository.get_instance()

    scenarios = scenario_repository.read_by_partial_name(PART_NAME)
    assert scenarios == []

    generate_random_records(scenario_repository, 1)
    for i in range(NUMBER_OF_RECORDS):
        scenario_mock.id = i + 1 + RANDOM_GENERATOR_MAX_RANGE
        scenario_mock.name = (
            "".join(random.choices(string.ascii_lowercase, k=5))
            + PART_NAME
            + "".join(random.choices(string.ascii_lowercase, k=5))
        )
        scenario_repository.create(scenario_mock)
    generate_random_records(
        scenario_repository, 1 + RANDOM_GENERATOR_MAX_RANGE + NUMBER_OF_RECORDS
    )
    scenarios = scenario_repository.read_by_partial_name(PART_NAME)
    assert len(scenarios) == NUMBER_OF_RECORDS


def test_read_by_id() -> None:
    scenario_mock = build_scenario_mock()
    initialize_db()

    scenario_repository = ScenarioRepository.get_instance()

    with pytest.raises(ScenarioException):
        scenario_repository.read_by_id(ID)

    generate_random_records(scenario_repository, 1)
    scenario = scenario_repository.create(scenario_mock)
    generate_random_records(scenario_repository, 1 + RANDOM_GENERATOR_MAX_RANGE)

    found_scenario = scenario_repository.read_by_id(ID)

    compare_scenarios(found_scenario, scenario)


def test_read_by_name() -> None:
    scenario_mock = build_scenario_mock()
    initialize_db()

    scenario_repository = ScenarioRepository.get_instance()

    with pytest.raises(ScenarioException):
        scenario_repository.read_by_name(NAME)

    generate_random_records(scenario_repository, 1)
    scenario = scenario_repository.create(scenario_mock)
    generate_random_records(scenario_repository, 1 + RANDOM_GENERATOR_MAX_RANGE)

    found_scenario = scenario_repository.read_by_name(NAME)

    compare_scenarios(found_scenario, scenario)


def test_update() -> None:
    scenario_mock = build_scenario_mock()
    initialize_db()

    scenario_repository = ScenarioRepository.get_instance()

    generate_random_records(scenario_repository, 1)
    scenario = scenario_repository.create(scenario_mock)
    generate_random_records(scenario_repository, 1 + RANDOM_GENERATOR_MAX_RANGE)

    scenario.name = "Changed name"
    scenario_repository.update(scenario)

    found_scenario = scenario_repository.read_by_id(ID)

    compare_scenarios(found_scenario, scenario)


def test_delete() -> None:
    scenario_mock = build_scenario_mock()
    initialize_db()

    scenario_repository = ScenarioRepository.get_instance()

    generate_random_records(scenario_repository, 1)
    scenario = scenario_repository.create(scenario_mock)
    generate_random_records(scenario_repository, 1 + RANDOM_GENERATOR_MAX_RANGE)

    scenario_repository.delete(scenario_mock)

    with pytest.raises(ScenarioException):
        scenario_repository.read_by_id(ID)


def initialize_db() -> None:
    database = peewee.SqliteDatabase(":memory:")
    database_proxy.initialize(database)

    database_proxy.create_tables(MODELS, safe=True)


def generate_random_records(
    scenario_repository: ScenarioRepository, start_id: int = 1
) -> None:
    scenario_mock_any = build_scenario_mock()
    scenario_mock_any.name = "Bad name"

    for i in range(random.randint(0, RANDOM_GENERATOR_MAX_RANGE)):
        scenario_mock_any.id = i + start_id
        if scenario_mock_any.id == ID:
            continue
        scenario_repository.create(scenario_mock_any)


def build_scenario_mock() -> mock.Mock:
    scenario_mock = mock.Mock(spec=Scenario)
    coordinates = mock.MagicMock(spec=Coordinates)
    coordinates.__str__.return_value = COORDINATES_STR

    scenario_mock.id = ID
    scenario_mock.name = NAME
    scenario_mock.coordinates = coordinates
    scenario_mock.restrictions = []
    return scenario_mock


def compare_scenarios(current: Scenario, expected: Scenario) -> None:
    assert current.id == expected.id
    assert current.name == expected.name
    assert str(current.coordinates) == str(expected.coordinates)
    assert current.restrictions == expected.restrictions
