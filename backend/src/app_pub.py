from __future__ import annotations
import os
import sys

current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(current_script_dir)
sys.path.append(project_root_dir)

from src.gloomhaven_model_pckg import database_proxy, MODELS
from src.gloomhaven_db_pckg import DbOptions, DbInitializer
from src.gloomhaven_pckg import AchievementRepository, ScenarioRepository
from src.gloomhaven_api_pckg import (
    AchievemenGetApi,
    ScenarioGetApi,
    GloomhavenApiFlaskWrapper,
)


db_options = DbOptions.create_from_environ()
DbInitializer.initialize_database_proxy(db_options, database_proxy, MODELS)

achievement_repository = AchievementRepository.get_instance()
scenario_repository = ScenarioRepository.get_instance()

achievement_api = AchievemenGetApi.create(achievement_repository)
scenario_api = ScenarioGetApi.create(scenario_repository)
apis = [achievement_api, scenario_api]

flask_wrapper = GloomhavenApiFlaskWrapper(database_proxy, apis)

app = flask_wrapper.app

if __name__ == "__main__":
    flask_wrapper.run()
