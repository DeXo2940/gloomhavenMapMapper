from __future__ import annotations
import peewee

from .model_exception import GloomhavenModelException
from pkg_resources import ensure_directory  # pip install pymysql require

# TODO: Don't define the DB here
database = peewee.MySQLDatabase(
    "gloomhaven",
    user="user",
    password="password",
    host="localhost",
    port=3306,
    autocommit=False,
)


class BaseModel(peewee.Model):
    class Meta:
        database = database

    @classmethod
    def get(cls, *query, **filters):
        try:
            return super().get(*query, **filters)
        except peewee.DoesNotExist:
            raise GloomhavenModelException(
                f"{cls.__name__} for query = `{query}` and filters = `{filters}` doesn't exist"
            )
