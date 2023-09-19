from __future__ import annotations
from functools import lru_cache

from ..gloomhaven_model_pckg import (
    Achievement as AchievementModel,
    GloomhavenModelException,
)
from .achievement_type import AchievementType
from .achievement import Achievement

from .gloomhaven_exception import AchievementException


class AchievementRepository:
    @lru_cache(maxsize=1)
    @staticmethod
    def get_instance() -> AchievementRepository:
        return AchievementRepository()

    def create(self, achievement: Achievement) -> Achievement:
        achievement_model = self._get_model(achievement)
        achievement_model.save(True)

        return self._get_from_model(achievement_model)

    def read(self) -> list[Achievement]:
        achievements = []
        query = AchievementModel.select().order_by(AchievementModel.id)
        for achievement_model in query:
            achievement = self._get_from_model(achievement_model)
            achievements.append(achievement)
        return achievements

    def read_by_partial_name(self, partial_name: str) -> list[Achievement]:
        achievements = []
        search_name = f"%{partial_name}%"
        query = (
            AchievementModel.select()
            .where(AchievementModel.name**search_name)
            .order_by(AchievementModel.id)
        )
        for achievement_model in query:
            achievement = self._get_from_model(achievement_model)
            achievements.append(achievement)
        return achievements

    def read_by_id(self, id: int) -> Achievement:
        try:
            achievement_model = AchievementModel.get(id=id)
            return self._get_from_model(achievement_model)
        except GloomhavenModelException:
            raise AchievementException(f"Achievement id=`{id}` doesn't exist")

    def read_by_name(self, name: str) -> Achievement:
        try:
            achievement_model = AchievementModel.get(name=name)
            return self._get_from_model(achievement_model)
        except GloomhavenModelException:
            raise AchievementException(f"Achievement `{name}` doesn't exist`")

    def update(self, achievement: Achievement) -> None:
        achievement_model = self._get_model(achievement)
        if achievement_model.save() != 1:
            raise AchievementException(
                f"Achievement id=`{achievement.id}` `{achievement.name}` couldn't be updated"
            )

    def delete(self, achievement: Achievement) -> None:
        achievement_model = self._get_model(achievement)
        achievement_model.delete_instance()

    def _get_model(self, achievement: Achievement) -> AchievementModel:
        id = achievement.id
        type_name = achievement.type.name
        name = achievement.name
        return AchievementModel(type=type_name, name=name, id=id)

    def _get_from_model(self, achievement_model: AchievementModel) -> Achievement:
        id = int(str(achievement_model.id))
        name = str(achievement_model.name)
        type_name = str(achievement_model.type)
        achievement_type = AchievementType.get(type_name)
        return Achievement.create(name, achievement_type, id)
