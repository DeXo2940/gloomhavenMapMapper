from __future__ import annotations
import peewee

from .base_model import BaseModel
from .fields import UnsignedTinyIntField
from .scenario import Scenario
from .achievement import Achievement


class Restriction(BaseModel):
    scenario = peewee.ForeignKeyField(
        Scenario, backref="restrictions", on_delete="CASCADE"
    )
    achievement = peewee.ForeignKeyField(Achievement, backref="restriction")
    is_done = peewee.BooleanField(null=False, default=False)
    level = UnsignedTinyIntField(null=True)

    class Meta:
        primary_key = peewee.CompositeKey("scenario", "achievement")
