from __future__ import annotations
import peewee

from .base_model import BaseModel
from .fields import LanguageCodeField
from .achievement import Achievement


class AchievementName(BaseModel):
    achievement = peewee.ForeignKeyField(
        Achievement,
        backref="name",
        on_delete="CASCADE",
    )
    # TODO Should get languages from somewhere else
    language = LanguageCodeField(null=False, default="EN")
    name = peewee.CharField(255, null=False, default="Tmp Achievement Name")

    class Meta:
        primary_key = peewee.CompositeKey("achievement", "language")
        indexes = ((("language", "name"), False),)
