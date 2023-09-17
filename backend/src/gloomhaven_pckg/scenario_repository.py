from __future__ import annotations
from functools import lru_cache

import peewee

from gloomhaven_model_pckg import (
    Scenario as ScenarioModel,
    Restriction as RestrictionModel,
    Achievement as AchievementModel,
)

from .scenario import Scenario
from .coordinates import Coordinates
from .restriction import Restriction
from .achievement import Achievement
from .achievement_type import AchievementType
from .gloomhaven_exception import ScenarioException


class ScenarioRepository:
    @lru_cache(maxsize=1)
    @staticmethod
    def get_instance() -> ScenarioRepository:
        return ScenarioRepository()

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        self._language = language

    def create(self, scenario: Scenario) -> Scenario:
        scenario_model = self._get_scenario_model(scenario)
        restriction_models = self._get_restriction_models(scenario)
        try:
            scenario_model.save(True)
        except peewee.IntegrityError:
            raise ScenarioException(f"Scenario id=`{scenario.id}` already exists")
        self._try_to_save_restrictions(restriction_models)
        new_scenario = self._get_scenario_from_model(scenario_model)
        restrictions = self._get_restrictions_from_from_model(restriction_models)
        new_scenario.restrictions = restrictions
        return new_scenario

    def read(self) -> list[Scenario]:
        query = self._get_select_query()
        return self._get_scenarios_from_select_query(query)

    def read_by_partial_name(self, partial_name: str) -> list[Scenario]:
        query_where = self._get_where_name_ilike(partial_name)
        query = self._get_select_query(query_where)
        return self._get_scenarios_from_select_query(query)

    def read_by_id(self, id: int) -> Scenario:
        query = self._get_select_id(id)
        if len(query) == 0:
            raise ScenarioException(f"Scenario id=`{id}` doesn't exist")
        scenario_model = query[0]
        scenario = self._get_scenario_from_model(scenario_model)
        restriction_models = scenario_model.restrictions
        restrictions = self._get_restrictions_from_from_model(restriction_models)
        scenario.restrictions = restrictions
        return scenario

    def read_by_name(self, name: str) -> Scenario:
        query = self._get_select_name(name)
        if len(query) == 0:
            raise ScenarioException(f"Scenario `{name}` doesn't exist")
        scenario_model = query[0]
        scenario = self._get_scenario_from_model(scenario_model)
        restriction_models = scenario_model.restrictions
        restrictions = self._get_restrictions_from_from_model(restriction_models)
        scenario.restrictions = restrictions
        return scenario

    def update(self, scenario: Scenario) -> None:
        scenario_model = self._get_scenario_model(scenario)
        restriction_models = self._get_restriction_models(scenario)

        scenario_model.save()
        RestrictionModel.delete().where(
            RestrictionModel.scenario == scenario_model
        ).execute()
        self._try_to_save_restrictions(restriction_models)

    def delete(self, scenario: Scenario) -> None:
        scenario_model = self._get_scenario_model(scenario)
        scenario_model.delete_instance()

    def _get_select_id(self, id: int) -> peewee.ModelSelect:
        where = self._get_where_id(id)
        return self._get_select_query(where)

    def _get_where_id(self, id: int) -> peewee.Expression:
        return ScenarioModel.id == id

    def _get_select_name(self, name: str) -> peewee.ModelSelect:
        where = self._get_where_name(name)
        return self._get_select_query(where)

    def _get_where_name(self, name: str) -> peewee.Expression:
        return ScenarioModel.name == name

    def _get_select_query(
        self, where: peewee.Expression | None = None
    ) -> peewee.ModelSelect:
        return (
            ScenarioModel.select()
            .join(RestrictionModel, peewee.JOIN.LEFT_OUTER)
            .where(where)
            .order_by(ScenarioModel.id)
        )

    def _get_where_name_ilike(self, partial_name: str) -> peewee.Expression:
        search_name = f"%{partial_name}%"
        return ScenarioModel.name**search_name

    def _get_scenarios_from_select_query(self, query) -> list[Scenario]:
        scenarios = []
        prev_scenario_model = None
        for scenario_model in query:
            if scenario_model == prev_scenario_model:
                continue
            scenario = self._get_scenario_from_model(scenario_model)
            restriction_models = scenario_model.restrictions
            restrictions = self._get_restrictions_from_from_model(restriction_models)
            scenario.restrictions = restrictions
            scenarios.append(scenario)
            prev_scenario_model = scenario_model
        return scenarios

    def _get_scenario_model(self, scenario: Scenario) -> ScenarioModel:
        id = scenario.id
        name = scenario.name
        coordinates = str(scenario.coordinates)
        return ScenarioModel(id=id, name=name, coordinates=coordinates)

    def _get_restriction_models(self, scenario: Scenario) -> list[RestrictionModel]:
        restriction_models = []
        restrictions = scenario.restrictions
        scenario_model = self._get_scenario_model(scenario)
        for restriction in restrictions:
            achievement = restriction.achievement
            is_done = restriction.is_done
            level = restriction.level
            achievement_model = self._get_achievement_model(achievement)
            restriction_model = RestrictionModel(
                scenario=scenario_model,
                achievement=achievement_model,
                is_done=is_done,
                level=level,
            )
            restriction_models.append(restriction_model)
        return restriction_models

    def _get_achievement_model(self, achievement: Achievement) -> AchievementModel:
        id = achievement.id
        type_name = achievement.type.name
        name = achievement.name
        return AchievementModel(type=type_name, name=name, id=id)

    def _get_scenario_from_model(self, scenario_model: ScenarioModel) -> Scenario:
        id = int(str(scenario_model.id))
        name = str(scenario_model.name)
        scenario_model_coordinates = scenario_model.coordinates
        coordinates = Coordinates.create_by_string(scenario_model_coordinates)
        return Scenario.create(id, coordinates, name)

    def _get_restrictions_from_from_model(
        self, restriction_models: list[RestrictionModel]
    ) -> list[Restriction]:
        restrictions = []
        for restriction_model in restriction_models:
            restriction = self._get_restriction_from_model(restriction_model)
            restrictions.append(restriction)
        return restrictions

    def _get_restriction_from_model(
        self, restriction_model: RestrictionModel
    ) -> Restriction:
        achievement_model = restriction_model.achievement
        achievement = self._get_achievement_from_model(achievement_model)

        is_done = bool(restriction_model.is_done)
        level = restriction_model.level
        if level is not None:
            level = int(str(level))
        return Restriction(achievement, is_done, level)

    def _get_achievement_from_model(
        self, achievement_model: AchievementModel | peewee.ForeignKeyField
    ) -> Achievement:
        id = achievement_model.id
        name = achievement_model.name
        type_name = str(achievement_model.type)
        achievement_type = AchievementType[type_name]
        return Achievement.create(name, achievement_type, id)

    def _try_to_save_restrictions(
        self, restriction_models: list[RestrictionModel]
    ) -> None:
        for restriction_model in restriction_models:
            try:
                restriction_model.save(True)
            except peewee.IntegrityError:
                raise ScenarioException(
                    f"Error durring Restriction creation for scenario id=`{restriction_model.scenario.id}`"
                    + f"\nSpecified restriction achievement doesn't exist, or same restriction is beeing inserted multiple times"
                )