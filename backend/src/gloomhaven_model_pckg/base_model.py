from __future__ import annotations
import peewee

from .model_exception import GloomhavenModelException
from pkg_resources import ensure_directory


database_proxy = peewee.DatabaseProxy()


class BaseModel(peewee.Model):
    class Meta:
        database = database_proxy

    @classmethod
    def get(cls, *query, **filters):
        try:
            return super().get(*query, **filters)
        except peewee.DoesNotExist:
            raise GloomhavenModelException(
                f"{cls.__name__} for query = `{query}` and filters = `{filters}` doesn't exist"
            )
