from __future__ import annotations
from functools import lru_cache
from typing import Any


import gloomhaven_model_pckg as model
from .achievement_type import AchievementType
from .achievement import Achievement

from .gloomhaven_exception import AchievementException


class AchievementRepository:
    def __init__(self, language: str):
        self.language = language
        # self.fallback_language = fallback_language

    # TODO should take language from somewhere else
    @lru_cache(maxsize=1)
    @staticmethod
    def get_instance(language: str = "PL") -> AchievementRepository:
        return AchievementRepository(language)

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        self._language = language

    # @property
    # def fallback_language(self) -> str:
    #     return self._fallback_language

    # @fallback_language.setter
    # def fallback_language(self, language: str) -> None:
    #     self._fallback_language = language

    def create(self, achievement: Achievement) -> Achievement:
        achievement_name_model = self._get_achievement_name_model(achievement)
        achievement_model = achievement_name_model.achievement

        achievement_model.save(True)
        achievement_name_model.save(True)

        return self._get_from_name_model(achievement_name_model)

    def read(self) -> list[Achievement]:
        achievements = []
        query = model.AchievementName.select()
        for achievement_name_model in query:
            achievement = self._get_from_name_model(achievement_name_model)
            achievements.append(achievement)
        return achievements

    def read_by_id(self, id: int) -> Achievement:
        tmp_achievement_model = model.Achievement(id=id)
        try:
            achievement_name_model = model.AchievementName.get(
                model.AchievementName.language == self.language,
                model.AchievementName.achievement == tmp_achievement_model,
            )

            return self._get_from_name_model(achievement_name_model)
        except model.GloomhavenModelException:
            raise AchievementException(
                f"Achievement id=`{id}` in `{self.language}` doesn't exist"
            )

    def read_by_name(self, name: str) -> Achievement:
        try:
            achievement_name_model = model.AchievementName.get(
                language=self.language, name=name
            )
            return self._get_from_name_model(achievement_name_model)
        except model.GloomhavenModelException:
            raise AchievementException(
                f"Achievement `{name}` doesn't exist in `{self.language}`"
            )

    def update(self, achievement: Achievement) -> None:
        achievement_name_model = self._get_achievement_name_model(achievement)
        achievement_model = achievement_name_model.achievement

        achievement_model.save()
        achievement_name_model.replace()

    def delete(self, achievement: Achievement) -> None:
        achievement_model = self._get_achievement_model(achievement)
        achievement_model.delete_instance()

    def _get_achievement_name_model(
        self, achievement: Achievement
    ) -> model.AchievementName:
        achievement_model = self._get_achievement_model(achievement)
        achievement_name = achievement.name

        return model.AchievementName(
            achievement=achievement_model, language=self.language, name=achievement_name
        )

    def _get_achievement_model(self, achievement: Achievement) -> model.Achievement:
        achievement_id = achievement.id
        achievement_type_name = achievement.type.name
        return model.Achievement(type=achievement_type_name, id=achievement_id)

    def _get_from_name_model(
        self,
        achievement_name_model: model.AchievementName,
    ):
        achievement_model = achievement_name_model.achievement
        achievement_id = achievement_model.id
        achievement_name = achievement_name_model.name
        achievement_type = AchievementType[str(achievement_model.type)]
        achievement = Achievement.create(
            achievement_name, achievement_type, achievement_id
        )
        return achievement
