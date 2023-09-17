from __future__ import annotations
import os


class DbOptions:
    def __init__(
        self,
        port: int | None,
        user: str | None,
        password: str | None,
        database: str | None,
        host: str | None,
    ) -> None:
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.host = host

    @staticmethod
    def create_from_environ() -> DbOptions:
        db_use_link = os.environ.get("DB_USE_LINK")
        port = os.environ.get("DB_PORT")
        if port is not None:
            port = int(str(port))
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        database = os.environ.get("DB_DATABASE")
        host = (
            "mysqldb"
            if db_use_link == True or db_use_link == "true"
            else os.environ.get("DB_HOST")
        )
        return DbOptions(port, user, password, database, host)

    def has_all_data(self) -> bool:
        return None not in (
            self.port,
            self.user,
            self.password,
            self.database,
            self.host,
        )
