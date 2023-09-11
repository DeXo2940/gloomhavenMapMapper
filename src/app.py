from __future__ import annotations
import os
import sys
from typing import Any, Callable
import flask
import uuid
import peewee

sys.path.append(os.path.dirname(__file__))

from gloomhaven_model_pckg import database_proxy, MODELS

from gloomhaven_pckg import (
    Achievement,
    AchievementRepository,
    ScenarioRepository,
    Scenario,
    GloomhavenException,
)


class GloomhavenApiException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


db_port = os.environ.get("DB_PORT")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_DATABASE")

db_use_link = os.environ.get("DB_USE_LINK")
db_host = "mysqldb" if db_use_link == True else os.environ.get("DB_HOST")

print(db_port, db_user, db_password, db_database, db_use_link, db_host)


if (
    db_port is not None
    and db_user is not None
    and db_password is not None
    and db_database is not None
    and db_host is not None
):
    database = peewee.MySQLDatabase(
        db_database,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        autoconnect=False,
    )
else:
    database = peewee.SqliteDatabase("gloomhaven.db")

database_proxy.initialize(database)

with database_proxy:
    database_proxy.create_tables(MODELS, safe=True)

achievement_repository = AchievementRepository.get_instance()
scenario_repository = ScenarioRepository.get_instance()

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.before_request
def _db_connect() -> None:
    database_proxy.connect()


@app.teardown_request
def _db_close(_) -> None:
    if not database_proxy.is_closed():
        database_proxy.close()


@app.route("/")
@app.route("/ping")
def ping() -> flask.Literal[str]:
    return "Gloomhaven Scenarios API is online"


@app.route("/achievements")
def get_achievements() -> flask.Response:
    return _try_for_exceptions_no_param(_get_all_achievements)


@app.route("/achievements(<id>)")
def get_achievement_by_id(id: int) -> flask.Response:
    return _try_for_exceptions_with_param(_find_achievement_by_id, id)


@app.route("/achievements", methods=["POST"])
def add_achievement() -> flask.Response:
    return _try_for_exceptions_no_param(_add_achievement)


@app.route("/achievements", methods=["PUT"])
def modify_achievement() -> flask.Response:
    return _try_for_exceptions_no_param(_modify_achievement)


@app.route("/scenarios")
def get_scenarios() -> flask.Response:
    return _try_for_exceptions_no_param(_find_all_scenarios)


@app.route("/scenarios(<id>)")
def get_scenario_by_id(id: int) -> flask.Response:
    return _try_for_exceptions_with_param(_find_scenario_by_id, id)


@app.route("/scenarios", methods=["POST"])
def add_scenarios() -> flask.Response:
    return _try_for_exceptions_no_param(_add_scenario)


@app.route("/scenarios", methods=["PUT"])
def modify_scenario() -> flask.Response:
    return _try_for_exceptions_no_param(_modify_scenario)


def _try_for_exceptions_with_param(
    callable_method: Callable[[Any], flask.Response], param: Any = None
) -> flask.Response:
    try:
        return callable_method(param)
    except GloomhavenException as gloomhaven_exception:
        return flask.Response(gloomhaven_exception.message, status=406)
    except GloomhavenApiException as gloomhaven_api_exception:
        return flask.Response(gloomhaven_api_exception.message, status=400)


def _try_for_exceptions_no_param(
    callable_method: Callable[[], flask.Response]
) -> flask.Response:
    try:
        return callable_method()
    except GloomhavenException as gloomhaven_exception:
        return flask.Response(gloomhaven_exception.message, status=406)
    except GloomhavenApiException as gloomhaven_api_exception:
        return flask.Response(gloomhaven_api_exception.message, status=400)


def _get_all_achievements() -> flask.Response:
    achievements = achievement_repository.read()
    return flask.jsonify([achievement.to_dict() for achievement in achievements])


def _find_achievement_by_id(id: int) -> flask.Response:
    achievement = achievement_repository.read_by_id(id)
    return flask.jsonify(achievement.to_dict())


def _add_achievement() -> flask.Response:
    achievement_json = _get_json_from_request()
    achievement = Achievement.create_from_dict(achievement_json)
    achievement = achievement_repository.create(achievement)
    return flask.jsonify(achievement.to_dict())


def _modify_achievement() -> flask.Response:
    achievement_json = _get_json_from_request()
    achievement = Achievement.create_from_dict(achievement_json)
    achievement_repository.update(achievement)
    return flask.jsonify(achievement.to_dict())


def _find_all_scenarios() -> flask.Response:
    scenarios = scenario_repository.read()
    return flask.jsonify([scenario.to_dict() for scenario in scenarios])


def _find_scenario_by_id(id: int) -> flask.Response:
    scenario = scenario_repository.read_by_id(id)
    return flask.jsonify(scenario.to_dict())


def _add_scenario() -> flask.Response:
    scenario_json = _get_json_from_request()
    scenario = Scenario.create_from_dict(scenario_json)
    scenario = scenario_repository.create(scenario)
    return flask.jsonify(scenario.to_dict())


def _modify_scenario() -> flask.Response:
    scenario_json = _get_json_from_request()
    scenario = Scenario.create_from_dict(scenario_json)
    scenario_repository.update(scenario)
    return flask.jsonify(scenario.to_dict())


def _get_json_from_request() -> dict[str, Any]:
    object_json = flask.request.get_json(silent=True)
    if object_json is None:
        raise GloomhavenApiException("Incorrect request body")
    return object_json


if __name__ == "__main__":
    app.run()
