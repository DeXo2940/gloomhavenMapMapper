from __future__ import annotations
import peewee

from .base_model import BaseModel


class Achievement(BaseModel):
    id = peewee.AutoField(null=False)
    name = peewee.CharField(255, null=False, default="Tmp Achievement Name", index=True)
    type = peewee.CharField(10, null=False)
