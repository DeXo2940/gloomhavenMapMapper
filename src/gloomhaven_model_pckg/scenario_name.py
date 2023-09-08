from __future__ import annotations
from email.policy import default
import peewee

from .base_model import BaseModel
from .fields import LanguageCodeField
from .scenario import Scenario


class ScenarioName(BaseModel):
    scenario = peewee.ForeignKeyField(Scenario, backref="name", on_delete="CASCADE")
    # TODO Should get languages from somewhere else
    language = LanguageCodeField(null=False, default="EN")
    name = peewee.CharField(null=False, default="Tmp Scenario Name")

    class Meta:
        primary_key = peewee.CompositeKey("scenario", "language")
        indexes = ((("language", "name"), False),)
