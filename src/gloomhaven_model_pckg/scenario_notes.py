from __future__ import annotations
import peewee

from .base_model import BaseModel
from .scenario import Scenario


class ScenarioNotes(BaseModel):
    scenario = peewee.ForeignKeyField(
        Scenario, backref="notes", primary_key=True, on_delete="CASCADE"
    )
    notes = peewee.TextField()
