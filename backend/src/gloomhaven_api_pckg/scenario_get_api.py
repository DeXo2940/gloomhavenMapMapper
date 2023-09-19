from __future__ import annotations
import flask

from ..gloomhaven_pckg import ScenarioRepository

from .safe_executioner import SafeExecutioner
from .gloomhaven_api import GloomhavenApi
from .api_method import ApiMethod
from .http_method import HttpMethod


class ScenarioGetApi(GloomhavenApi):
    ENDPOINT = "scenarios"

    def __init__(self, scenario_repository: ScenarioRepository) -> None:
        self._repository = scenario_repository

    @staticmethod
    def create(scenario_repository: ScenarioRepository) -> ScenarioGetApi:
        return ScenarioGetApi(scenario_repository)

    def get_endpoint(self) -> str:
        return ScenarioGetApi.ENDPOINT

    def get_path(self) -> str:
        return f"/{ScenarioGetApi.ENDPOINT}"

    def get_avaliable_methods(self) -> list[ApiMethod]:
        api_get_method = ApiMethod(HttpMethod.GET, self.get)
        api_get_one_method = ApiMethod(HttpMethod.GET, self.get_one, "<int:id>", "one")
        return [api_get_method, api_get_one_method]

    def get(self) -> flask.Response:
        search_name = flask.request.args.get("name")
        if search_name is not None:
            return SafeExecutioner.execute_with_param(
                self._get_scenario_by_partial_name, search_name
            )
        return SafeExecutioner.execute_no_param(self._get_all_scenarios)

    def get_one(self, id: int) -> flask.Response:
        return SafeExecutioner.execute_with_param(self._get_scenario_by_id, id)

    def _get_scenario_by_partial_name(self, partial_name: str) -> flask.Response:
        scenarios = self._repository.read_by_partial_name(partial_name)
        return flask.jsonify([scenario.to_dict() for scenario in scenarios])

    def _get_all_scenarios(self) -> flask.Response:
        scenarios = self._repository.read()
        return flask.jsonify([scenario.to_dict() for scenario in scenarios])

    def _get_scenario_by_id(self, id: int) -> flask.Response:
        scenario = self._repository.read_by_id(id)
        return flask.jsonify(scenario.to_dict())
