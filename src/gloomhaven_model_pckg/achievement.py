from __future__ import annotations
import peewee

from .base_model import BaseModel


class Achievement(BaseModel):
    id = peewee.AutoField(null=False)
    type = peewee.CharField(10, null=False)
