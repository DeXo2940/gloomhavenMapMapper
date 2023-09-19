from __future__ import annotations
import flask


from ..gloomhaven_pckg import Scenario, ScenarioRepository

from .scenario_get_api import ScenarioGetApi
from .safe_executioner import SafeExecutioner
from .request_json import RequestJson
from .api_method import ApiMethod
from .http_method import HttpMethod


class ScenarioApi(ScenarioGetApi):
    def __init__(self, scenario_repository: ScenarioRepository) -> None:
        super().__init__(scenario_repository)

    @staticmethod
    def create(scenario_repository: ScenarioRepository) -> ScenarioApi:
        return ScenarioApi(scenario_repository)

    def post(self) -> flask.Response:
        return SafeExecutioner.execute_no_param(self._add_scenario)

    def put(self) -> flask.Response:
        return SafeExecutioner.execute_no_param(self._modify_scenario)

    def get_avaliable_methods(self) -> list[ApiMethod]:
        api_post_method = ApiMethod(HttpMethod.POST, self.post)
        api_put_method = ApiMethod(HttpMethod.PUT, self.put)
        return super().get_avaliable_methods() + [api_post_method, api_put_method]

    def _add_scenario(self) -> flask.Response:
        scenario_json = RequestJson.get_json_from_request()
        scenario = Scenario.create_from_dict(scenario_json)
        scenario = self._repository.create(scenario)
        return flask.jsonify(scenario.to_dict())

    def _modify_scenario(self) -> flask.Response:
        scenario_json = RequestJson.get_json_from_request()
        scenario = Scenario.create_from_dict(scenario_json)
        self._repository.update(scenario)
        return flask.jsonify(scenario.to_dict())
