from __future__ import annotations
import flask

from gloomhaven_pckg import Achievement, AchievementRepository

from .achievement_get_api import AchievemenGetApi
from .safe_executioner import SafeExecutioner
from .request_json import RequestJson
from .api_method import ApiMethod


class AchievemenApi(AchievemenGetApi):
    def __init__(self, achievement_repository: AchievementRepository) -> None:
        super().__init__(achievement_repository)

    @staticmethod
    def create(achievement_repository: AchievementRepository) -> AchievemenApi:
        return AchievemenApi(achievement_repository)

    def get_avaliable_methods(self) -> list[ApiMethod]:
        api_post_method = ApiMethod(ApiMethod.POST, self.post)
        api_put_method = ApiMethod(ApiMethod.PUT, self.put)
        return super().get_avaliable_methods() + [api_post_method, api_put_method]

    def post(self) -> flask.Response:
        return SafeExecutioner.execute_no_param(self._add_achievement)

    def put(self) -> flask.Response:
        return SafeExecutioner.execute_no_param(self._modify_achievement)

    def _add_achievement(self) -> flask.Response:
        achievement_json = RequestJson.get_json_from_request()
        achievement = Achievement.create_from_dict(achievement_json)
        achievement = self._repository.create(achievement)
        return flask.jsonify(achievement.to_dict())

    def _modify_achievement(self) -> flask.Response:
        achievement_json = RequestJson.get_json_from_request()
        achievement = Achievement.create_from_dict(achievement_json)
        self._repository.update(achievement)
        return flask.jsonify(achievement.to_dict())
