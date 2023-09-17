from __future__ import annotations
from typing import Any, Callable
import flask

from .gloomhaven_api_exception import GloomhavenApiException


class RequestJson:
    @staticmethod
    def get_json_from_request() -> dict[str, Any]:
        object_json = flask.request.get_json(silent=True)
        if object_json is None:
            raise GloomhavenApiException("Incorrect request body")
        return object_json
