from __future__ import annotations
from typing import Any, Callable
import flask

from gloomhaven_pckg import GloomhavenException
from .gloomhaven_api_exception import GloomhavenApiException


class SafeExecutioner:
    @staticmethod
    def execute_with_param(
        callable_method: Callable[[Any], flask.Response], param: Any
    ) -> flask.Response:
        try:
            return callable_method(param)
        except GloomhavenException as gloomhaven_exception:
            return flask.Response(gloomhaven_exception.message, status=406)
        except GloomhavenApiException as gloomhaven_api_exception:
            return flask.Response(gloomhaven_api_exception.message, status=400)
        except Exception:
            return flask.Response("Unknown exception occured", status=500)

    @staticmethod
    def execute_no_param(
        callable_method: Callable[[], flask.Response]
    ) -> flask.Response:
        try:
            return callable_method()
        except GloomhavenException as gloomhaven_exception:
            return flask.Response(gloomhaven_exception.message, status=406)
        except GloomhavenApiException as gloomhaven_api_exception:
            return flask.Response(gloomhaven_api_exception.message, status=400)
        except Exception:
            return flask.Response("Unknown exception occured", status=500)
