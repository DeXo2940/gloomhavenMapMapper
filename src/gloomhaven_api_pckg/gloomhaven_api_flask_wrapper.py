from __future__ import annotations

import flask
import peewee
import uuid

from .gloomhaven_api import GloomhavenApi


class GloomhavenApiFlaskWrapper:
    def __init__(
        self, database: peewee.DatabaseProxy, callable_apis: list[GloomhavenApi]
    ) -> None:
        self._init_app()

        self._database = database
        self._apis = callable_apis

        self._register_routes()

    @staticmethod
    def create(
        database: peewee.DatabaseProxy, callable_apis: list[GloomhavenApi]
    ) -> GloomhavenApiFlaskWrapper:
        return GloomhavenApiFlaskWrapper(database, callable_apis)

    @property
    def app(self) -> flask.Flask:
        return self._app

    def _init_app(self) -> None:
        self._app = flask.Flask(__name__)
        self._app.secret_key = str(uuid.uuid4())
        print(__name__)

    def _register_routes(self) -> None:
        self._app.before_request(self._db_connect)
        self._app.teardown_request(self._db_close)

        self._app.route("/")(self._ping)
        self._app.route("/ping")(self._ping)

        for api in self._apis:
            api_methods = api.get_avaliable_methods()
            for api_method in api_methods:
                self._app.add_url_rule(
                    f"{api.get_path()}{api_method.parameters}",
                    endpoint=f"{api.get_endpoint()}{api_method.endpoint_sufix}",
                    methods=[api_method.http_method],
                    view_func=api_method.callable_method,
                )

    def _db_connect(self) -> None:
        self._database.connect()

    def _db_close(self, _) -> None:
        if not self._database.is_closed():
            self._database.close()

    def _ping(self) -> flask.Literal:
        return "Gloomhaven API is online"

    def run(self) -> None:
        self._app.run()
