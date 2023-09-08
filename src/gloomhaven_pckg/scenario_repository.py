from __future__ import annotations
from functools import lru_cache

import peewee

import gloomhaven_model_pckg as model


from .scenario import Scenario
from .coordinates import Coordinates
from .requirement import Requirement
from .achievement import Achievement
from .achievement_type import AchievementType
from .gloomhaven_exception import ScenarioException


class ScenarioRepository:
    _QUERY_SELECT = (
        model.Restriction.is_done,
        model.Restriction.level,
        model.Scenario.id,
        model.Scenario.coordinates,
        model.ScenarioName.name,
        model.ScenarioNotes.notes,
        model.Achievement.id,
        model.Achievement.type,
        model.AchievementName.name,
    )

    def __init__(self, language: str) -> None:
        self.language = language

    # TODO should take language from somewhere else
    @lru_cache(maxsize=1)
    @staticmethod
    def get_instance(language: str = "PL") -> ScenarioRepository:
        return ScenarioRepository(language)

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        self._language = language

    def create(self, scenario: Scenario) -> Scenario:
        scenario_name_model = self._get_scenario_name_model(scenario)
        scenario_model = scenario_name_model.scenario
        scenario_notes_model = self._get_scenario_notes_model(scenario)
        restriction_models = self._get_restriction_models(scenario)

        scenario_model.save(True)
        scenario_name_model.save(True)
        scenario_notes_model.save(True)
        for restriction_model in restriction_models:
            restriction_model.save(True)
        # TODO I don't need to read all of that
        # - I should have everything except achievement id
        return self.read_by_id(scenario.id)

    def read(self) -> list[Scenario]:
        pass  # TODO
        scenarios = []
        # query = model.ScenarioName.select()
        # for scenario_name_model in query:
        #     scenario = self._get_from_name_model(scenario_name_model)
        #     scenarios.append(scenario)
        return scenarios

    def read_by_id(self, id: int) -> Scenario:
        select_query = self._create_select_query_where_id(id)
        scenario: Scenario | None = None

        cursor = model.db.execute(select_query)
        for row_tuple in cursor:
            if scenario is None:
                scenario = self._get_scenario_from_row_tuple(row_tuple)
            restriction = self._get_restriction_from_row_tuple(row_tuple)
            if restriction is not None:
                scenario.add_blocker(restriction)
        if scenario is None:
            raise ScenarioException(
                f"Scenario id=`{id}` in `{self.language}` doesn't exist"
            )
        return scenario

    def read_by_name(self, name: str) -> Scenario:
        select_query = self._create_select_query_where_name(name)

        cursor = model.db.execute(select_query)
        scenario: Scenario | None = None
        for row_tuple in cursor:
            if scenario is None:
                scenario = self._get_scenario_from_row_tuple(row_tuple)
            restriction = self._get_restriction_from_row_tuple(row_tuple)
            if restriction is not None:
                scenario.add_blocker(restriction)
        if scenario is None:
            raise ScenarioException(
                f"Scenario `{name}` doesn't exist in `{self.language}`"
            )
        return scenario

    def update(self, scenario: Scenario) -> None:
        scenario_name_model = self._get_scenario_name_model(scenario)
        scenario_model = scenario_name_model.scenario
        scenario_notes_model = self._get_scenario_notes_model(scenario)
        restriction_models = self._get_restriction_models(scenario)

        scenario_model.save()
        scenario_name_model.replace()
        scenario_notes_model.replace()

        for restriction_model in restriction_models:
            restriction_model.replace()

    def delete(self, scenario: Scenario) -> None:
        achievement_model = self._get_scenario_model(scenario)
        achievement_model.delete_instance()

    def _get_scenario_name_model(self, scenario: Scenario) -> model.ScenarioName:
        scenario_model = self._get_scenario_model(scenario)
        scenario_name = scenario.name
        return model.ScenarioName(
            scenario=scenario_model, language=self.language, name=scenario_name
        )

    def _get_scenario_notes_model(self, scenario: Scenario) -> model.ScenarioNotes:
        scenario_model = self._get_scenario_model(scenario)
        scenario_notes = scenario.notes
        return model.ScenarioNotes(scenario=scenario_model, notes=scenario_notes)

    def _get_restriction_models(self, scenario: Scenario) -> list[model.Restriction]:
        scenario_model = self._get_scenario_model(scenario)
        restriction_models = []
        for restriction in scenario.blockers:
            restriction_model = self._get_restriction_model(restriction, scenario_model)
            restriction_models.append(restriction_model)
        return restriction_models

    def _get_restriction_model(
        self, restriction: Requirement, scenario_model: model.Scenario
    ) -> model.Restriction:
        restriction_is_done = restriction.is_done
        restriction_level = restriction.level
        restriction_achievement = restriction.achievement
        tmp_achievement_model = model.Achievement(id=restriction_achievement.id)
        return model.Restriction(
            scenario=scenario_model,
            achievement=tmp_achievement_model,
            is_done=restriction_is_done,
            level=restriction_level,
        )

    def _get_scenario_model(self, scenario: Scenario) -> model.Scenario:
        scenario_id = scenario.id
        scenario_coordinates = str(scenario.coordinates)
        return model.Scenario(id=scenario_id, coordinates=scenario_coordinates)

    def _create_select_query_where_id(self, id: int) -> peewee.ModelSelect:
        query_where = self._create_query_where_language_id(id)
        return self._create_select_query(query_where)

    def _create_query_where_language_id(self, id: int) -> peewee.Expression:
        query_where_language = self._create_query_where_language()
        return (
            model.Restriction.scenario == model.Scenario(id=id)
        ) & query_where_language

    def _create_select_query_where_name(self, name: str) -> peewee.ModelSelect:
        query_where = self._create_query_where_language_name(name)
        return self._create_select_query(query_where)

    def _create_query_where_language_name(self, name: str) -> peewee.Expression:
        query_where_language = self._create_query_where_language()
        return (
            model.ScenarioName.name == model.Scenario(id=name)
        ) & query_where_language

    def _create_query_where_language(self) -> peewee.Expression:
        return (model.ScenarioName.language == self._language) & (
            (model.AchievementName.language == self._language)
            | (model.AchievementName.language == None)
        )

    def _create_select_query(
        self, query_where: peewee.Expression
    ) -> peewee.ModelSelect:
        return (
            model.Restriction.select(*ScenarioRepository._QUERY_SELECT)
            .join(model.Scenario, peewee.JOIN.RIGHT_OUTER)
            .join(model.ScenarioName)
            .switch(model.Scenario)
            .join(model.ScenarioNotes, peewee.JOIN.LEFT_OUTER)
            .switch(model.Restriction)
            .join(model.Achievement, peewee.JOIN.LEFT_OUTER)
            .join(model.AchievementName, peewee.JOIN.LEFT_OUTER)
            .where(query_where)
        )

    def _get_scenario_from_row_tuple(
        self, row_tuple: tuple[bool, int, int, str, str, str, int, str, str]
    ) -> Scenario:
        scenario_tuple = self._get_scenario_tuple_from_row_tuple(row_tuple)
        return self._get_scenario_from_tuple(scenario_tuple)

    def _get_scenario_tuple_from_row_tuple(
        self, row_tuple: tuple[bool, int, int, str, str, str, int, str, str]
    ) -> tuple[int, str, str, str]:
        (_, _, id, coords, name, notes, _, _, _) = row_tuple
        return (id, coords, name, notes)

    def _get_scenario_from_tuple(
        self, scenario_tuple: tuple[int, str, str, str]
    ) -> Scenario:
        id, coords, name, notes = scenario_tuple
        coords = Coordinates.create_by_string(coords)
        scenario = Scenario.create(id, coords, name)
        scenario.notes = notes
        return scenario

    def _get_restriction_from_row_tuple(
        self, row_tuple: tuple[bool, int, int, str, str, str, int, str, str]
    ) -> Requirement | None:
        achievement_tuple = self._get_achievement_tuple_from_row_tuple(row_tuple)
        if achievement_tuple[0] is None:
            return None
        restriction_tuple = self._get_restriction_tuple_from_row_tuple(row_tuple)
        return self._get_restriction_from_tuple(restriction_tuple, achievement_tuple)

    def _get_achievement_tuple_from_row_tuple(
        self, row_tuple: tuple[bool, int, int, str, str, str, int, str, str]
    ) -> tuple[int, str, str]:
        (_, _, _, _, _, _, id, type, name) = row_tuple
        return (id, name, type)

    def _get_restriction_tuple_from_row_tuple(
        self, row_tuple: tuple[bool, int, int, str, str, str, int, str, str]
    ) -> tuple[bool, int]:
        (is_done, level, _, _, _, _, _, _, _) = row_tuple
        return (is_done, level)

    def _get_restriction_from_tuple(
        self,
        restriction_tuple: tuple[bool, int],
        achievement_tuple: tuple[int, str, str],
    ) -> Requirement:
        (is_done, level) = restriction_tuple
        achievement = self._get_achievement_from_tuple(achievement_tuple)
        return Requirement.create(achievement, is_done, level)

    def _get_achievement_from_tuple(
        self, achievement_tuple: tuple[int, str, str]
    ) -> Achievement:
        (id, name, type) = achievement_tuple
        achievement_type = AchievementType[type]
        return Achievement.create(name, achievement_type, id)
