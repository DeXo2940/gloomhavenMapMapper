from __future__ import annotations
import peewee

from .base_model import BaseModel
from .fields import UnsignedTinyIntField


class Scenario(BaseModel):
    id = UnsignedTinyIntField(null=True, primary_key=True)
    name = peewee.CharField(null=False, default="Tmp Scenario Name", index=True)
    coordinates = peewee.CharField(4, null=True, default="A-1")
