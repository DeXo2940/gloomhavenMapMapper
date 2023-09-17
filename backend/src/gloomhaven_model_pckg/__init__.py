from .base_model import database_proxy
from .scenario import Scenario
from .achievement import Achievement
from .restriction import Restriction
from .model_exception import GloomhavenModelException

MODELS = [
    Scenario,
    Achievement,
    Restriction,
]
