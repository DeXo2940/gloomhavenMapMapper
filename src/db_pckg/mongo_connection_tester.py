from __future__ import annotations

from pymongo import MongoClient, errors, timeout

from .db_exceptions import DbException


class MongoConnectionTester:
    def __init__(
        self,
        client: MongoClient,
        connection_string: str,
        test_timeout_ms: int,
        connection_retries: int,
    ) -> None:
        self._client = client
        self._connection_string = connection_string
        self._test_timeout_ms = test_timeout_ms
        self._validate_retries(connection_retries)
        self._connection_retries = connection_retries

    @staticmethod
    def create(
        client: MongoClient,
        connection_string: str,
        test_timeout_ms: int,
        connection_retries: int,
    ) -> MongoConnectionTester:
        return MongoConnectionTester(
            client, connection_string, test_timeout_ms, connection_retries
        )

    def test_connection(self) -> None:
        if not self._is_connection_ok():
            raise DbException(
                f"Couldn't connect to database at: {self._connection_string}"
            )

    def _validate_retries(self, retries: int) -> None:
        if retries < 0:
            raise DbException(f"Invalid number of connection retries passed: {retries}")

    def _is_connection_ok(self) -> bool:
        for _ in range(self._connection_retries + 1):
            if self._is_single_connection_try_ok():
                return True
        return False

    def _is_single_connection_try_ok(self) -> bool:
        try:
            with timeout(self._test_timeout_ms / 1000):
                self._client.admin.command("ping")
            return True
        except errors.ServerSelectionTimeoutError:
            return False
