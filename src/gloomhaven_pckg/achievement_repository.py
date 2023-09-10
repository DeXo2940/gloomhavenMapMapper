from __future__ import annotations
from functools import lru_cache

import gloomhaven_model_pckg as model
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
        query = model.Achievement.select()
        for achievement_model in query:
            achievement = self._get_from_model(achievement_model)
            achievements.append(achievement)
        return achievements

    def read_by_id(self, id: int) -> Achievement:
        try:
            achievement_model = model.Achievement.get(id=id)
            return self._get_from_model(achievement_model)
        except model.GloomhavenModelException:
            raise AchievementException(f"Achievement id=`{id}` doesn't exist")

    def read_by_name(self, name: str) -> Achievement:
        try:
            achievement_model = model.Achievement.get(name=name)
            return self._get_from_model(achievement_model)
        except model.GloomhavenModelException:
            raise AchievementException(f"Achievement `{name}` doesn't exist`")

    def update(self, achievement: Achievement) -> None:
        achievement_model = self._get_model(achievement)
        if achievement_model.save() != 1:
            raise AchievementException(
                f"Achievement id=`{achievement.id}` `{achievement.name}` couldn't be updated exist"
            )

    def delete(self, achievement: Achievement) -> None:
        achievement_model = self._get_model(achievement)
        achievement_model.delete_instance()

    def _get_model(self, achievement: Achievement) -> model.Achievement:
        id = achievement.id
        type_name = achievement.type.name
        name = achievement.name
        return model.Achievement(type=type_name, name=name, id=id)

    def _get_from_model(self, achievement_model: model.Achievement) -> Achievement:
        id = achievement_model.id
        name = achievement_model.name
        type_name = str(achievement_model.type)
        achievement_type = AchievementType[type_name]
        return Achievement.create(name, achievement_type, id)
