from __future__ import annotations
import peewee


class UnsignedTinyIntField(peewee.IntegerField):
    field_type = "TINYINT UNSIGNED"


class LanguageCodeField(peewee.FixedCharField):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(max_length=2, *args, **kwargs)
