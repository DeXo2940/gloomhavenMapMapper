from __future__ import annotations
from typing import Any, Callable
import flask
import uuid

from db_pckg import DbException, DbFilter, MongoDbAccess, MognoDbFilter, MongoDbAccess


from gloomhaven_scenarios_pckg import (
    ScenarioDAO,
    Scenario,
    Coordinates,
    Achievement,
    AchievementType,
    AchievementDAO,
    Requirement,
    GloomhavenException,
)


CONNECTION_STRING = "mongodb://localhost:27017/"
DB_NAME = "gloomhaven_db"

# or perhaps should be:
#
# mongo_db_access = MongoDbAccess.create(CONNECTION_STRING, DB_NAME)
#
# to have one db_access through all DAOs
# and then all calls id DAOs would need to call the db_access with collection name?
# but that would mean, that the methods accept collection name/table name,
# but the name would need to suggest that both are correct depending on the implementation


def _create_db_access(collection_name: str) -> MongoDbAccess:
    return MongoDbAccess.create(CONNECTION_STRING, DB_NAME, collection_name)


mongo_db_achievement_access = _create_db_access(AchievementDAO.COLLECTION_NAME)
achievement_dao = AchievementDAO.get_instance(mongo_db_achievement_access)

mongo_db_scenario_access = _create_db_access(ScenarioDAO.COLLECTION_NAME)
scenario_dao = ScenarioDAO.get_instance(mongo_db_scenario_access, achievement_dao)


app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route("/")
@app.route("/ping")
def ping() -> flask.Literal[str]:
    return "Gloomhaven Scenarios API is online"


@app.route("/achievements")
def get_achievements() -> flask.Response:
    return _try_for_exceptions_no_param(_find_all_achievements)


@app.route("/achievements", methods=["POST"])
def add_achievement() -> flask.Response:
    achievement_json = flask.request.get_json(silent=True)
    if achievement_json is None:
        return _incorrect_json_error()

    return _try_for_exceptions_with_param(_save_achievement, achievement_json)


@app.route("/scenarios")
def get_scenarios() -> flask.Response:
    return _try_for_exceptions_no_param(_find_all_scenarios)


@app.route("/scenarios(<id>)")
def get_scenario_by_id(id: int) -> flask.Response:
    return _try_for_exceptions_with_param(_find_scenario_by_id, id)


@app.route("/scenarios", methods=["POST"])
def add_scenarios() -> flask.Response:
    scenario_json = flask.request.get_json(silent=True)
    if scenario_json is None:
        return _incorrect_json_error()

    return _try_for_exceptions_with_param(_save_scenario, scenario_json)


def _try_for_exceptions_with_param(
    callable_method: Callable[[Any], flask.Response], param: Any = None
) -> flask.Response:
    try:
        return callable_method(param)
    except GloomhavenException as gloomhaven_exception:
        return flask.Response(gloomhaven_exception.message, status=406)
    except DbException as db_exception:
        return flask.Response(db_exception.message, status=503)


def _try_for_exceptions_no_param(
    callable_method: Callable[[], flask.Response]
) -> flask.Response:
    try:
        return callable_method()
    except GloomhavenException as gloomhaven_exception:
        return flask.Response(gloomhaven_exception.message, status=406)
    except DbException as db_exception:
        return flask.Response(db_exception.message, status=503)


def _find_all_achievements() -> flask.Response:
    achievements = achievement_dao.find_all()
    achievement_dicts = [achievement.to_dict() for achievement in achievements]
    return flask.jsonify(achievement_dicts)


def _save_achievement(object_json: Any) -> flask.Response:
    achievement = Achievement.create_from_dict(object_json)
    achievement_dao.save_one(achievement)
    return flask.Response(repr(achievement), status=201)


def _find_all_scenarios() -> flask.Response:
    scenarios = scenario_dao.find_all()
    scenario_dicts = [scenario.to_dict() for scenario in scenarios]

    for scenario_dict in scenario_dicts:
        blockers = scenario_dict.get("blockers")
        if blockers is None:
            continue
        for restriction in blockers:
            restriction.get("")

    return flask.jsonify(scenario_dicts)


def _find_scenario_by_id(id: int) -> flask.Response:
    scenario = scenario_dao.find_by_id(id)
    return flask.Response(repr(scenario), status=201)


def _save_scenario(object_json: Any) -> flask.Response:
    scenario = Scenario.create_from_dict(object_json, achievement_dao)
    scenario_dao.save_one(scenario)
    return flask.Response(repr(scenario), status=201)


def _incorrect_json_error() -> flask.Response:
    return flask.Response("Incorrect request body", status=400)


if __name__ == "__main__":
    app.run()
