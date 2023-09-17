from __future__ import annotations
import flask

from gloomhaven_pckg import AchievementRepository

from .safe_executioner import SafeExecutioner
from .gloomhaven_api import GloomhavenApi
from .api_method import ApiMethod
from .http_method import HttpMethod


class AchievemenGetApi(GloomhavenApi):
    ENDPOINT = "achievements"

    def __init__(self, achievement_repository: AchievementRepository) -> None:
        self._repository = achievement_repository

    @staticmethod
    def create(achievement_repository: AchievementRepository) -> AchievemenGetApi:
        return AchievemenGetApi(achievement_repository)

    def get_endpoint(self) -> str:
        return AchievemenGetApi.ENDPOINT

    def get_path(self) -> str:
        return f"/{AchievemenGetApi.ENDPOINT}"

    def get_avaliable_methods(self) -> list[ApiMethod]:
        api_get_method = ApiMethod(HttpMethod.GET, self.get)
        api_get_one_method = ApiMethod(HttpMethod.GET, self.get_one, "<int:id>", "one")
        return [api_get_method, api_get_one_method]

    def get(self) -> flask.Response:
        search_name = flask.request.args.get("name")
        if search_name is not None:
            return SafeExecutioner.execute_with_param(
                self._get_achievements_by_partial_name, search_name
            )
        return SafeExecutioner.execute_no_param(self._get_all_achievements)

    def get_one(self, id: int) -> flask.Response:
        return SafeExecutioner.execute_with_param(self._get_achievement_by_id, id)

    def _get_achievements_by_partial_name(self, partial_name: str) -> flask.Response:
        achievements = self._repository.read_by_partial_name(partial_name)
        return flask.jsonify([achievement.to_dict() for achievement in achievements])

    def _get_all_achievements(self) -> flask.Response:
        achievements = self._repository.read()
        return flask.jsonify([achievement.to_dict() for achievement in achievements])

    def _get_achievement_by_id(self, id: int) -> flask.Response:
        achievement = self._repository.read_by_id(id)
        return flask.jsonify(achievement.to_dict())
