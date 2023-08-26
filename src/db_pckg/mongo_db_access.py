from __future__ import annotations
from typing import Any

import pymongo
import pymongo.errors as pymongo_error
import pymongo.collection as pymongo_coll
import pymongo.database as pymongo_db

from .db_structure import DbStructure
from .db_filter import DbFilter
from .mongo_db_filter import MognoDbFilter
from .db_structure import DbStructure
from .db_exceptions import DbException
from .db_access import DbAccess
from .mongo_connection_tester import MongoConnectionTester


class MongoDbAccess(DbAccess):
    TEST_TIMEOUT_MS = 100
    TIMEOUT_MS = 5_000

    def __init__(
        self,
        connection_string: str,
        database_name: str,
        collection_name: str,
        timeout_ms: int = TIMEOUT_MS,
        test_timeout_ms: int = TEST_TIMEOUT_MS,
        connection_retries: int = 0,
    ) -> None:
        self._client = pymongo.MongoClient(
            connection_string, serverSelectionTimeoutMS=timeout_ms
        )
        connection_tester = MongoConnectionTester.create(
            self._client, connection_string, test_timeout_ms, connection_retries
        )
        connection_tester.test_connection()

        self._database: pymongo_db.Database[Any] = self._client[database_name]
        self._collection: pymongo_coll.Collection[Any] = self._database[collection_name]

    @staticmethod
    def create(
        connection_string: str,
        database_name: str,
        collection_name: str,
        timeout_ms: int = TIMEOUT_MS,
        test_timeout_ms: int = TEST_TIMEOUT_MS,
        connection_retries: int = 0,
    ) -> MongoDbAccess:
        return MongoDbAccess(
            connection_string,
            database_name,
            collection_name,
            timeout_ms,
            test_timeout_ms,
            connection_retries,
        )

    def find_single(self, key: DbFilter) -> dict[str, Any]:
        mongo_key = self._translate_to_mongo_filter(key)
        key_dict = mongo_key.translate_for_db()
        try:
            record = self._collection.find_one(key_dict)
            return record if record != None else {}
        except pymongo_error.ServerSelectionTimeoutError:
            raise DbException("Server Database Timeout")

    def find(self, filter: DbFilter | None = None) -> list[dict[str, Any]]:
        try:
            if filter is None:
                records = self._collection.find()
                return list(records)
            mongo_filter = self._translate_to_mongo_filter(filter)
            filter_dict = mongo_filter.translate_for_db()

            records = self._collection.find(filter_dict)
            return list(records)
        except pymongo_error.ServerSelectionTimeoutError:
            raise DbException("Server Database Timeout")

    def update(self, object: DbStructure) -> None:
        key_filter = self._get_object_key_dict(object)
        object_dict = self._get_cleaned_dict(object)
        try:
            self._collection.replace_one(key_filter, object_dict, True)
        except pymongo_error.ServerSelectionTimeoutError:
            raise DbException("Server Database Timeout")

    def update_bulk(self, objects: list[DbStructure]) -> None:
        bulk_operations = []
        for object in objects:
            replace_one = self._get_replace_one_for_bulk(object)
            bulk_operations.append(replace_one)
        try:
            self._collection.bulk_write(bulk_operations)
        except pymongo_error.ServerSelectionTimeoutError:
            raise DbException("Server Database Timeout")

    def delete(self, object: DbStructure) -> None:
        key_filter = self._get_object_key_dict(object)
        try:
            self._collection.delete_one(key_filter)
        except pymongo_error.ServerSelectionTimeoutError:
            raise DbException("Server Database Timeout")

    def delete_bulk(self, objects: list[DbStructure]) -> None:  # TODO implement
        bulk_operations = []
        for object in objects:
            delete_one = self._get_delete_one_for_bulk(object)
            bulk_operations.append(delete_one)
        try:
            self._collection.bulk_write(bulk_operations)
        except pymongo_error.ServerSelectionTimeoutError:
            raise DbException("Server Database Timeout")

    def _translate_to_mongo_filter(self, filter: DbFilter) -> MognoDbFilter:
        return (
            filter
            if isinstance(filter, MognoDbFilter)
            else MognoDbFilter.create_by_generic(filter)
        )

    def _get_delete_one_for_bulk(self, object: DbStructure) -> pymongo.DeleteOne:
        key_filter = self._get_object_key_dict(object)
        return pymongo.DeleteOne(key_filter)

    def _get_replace_one_for_bulk(self, object: DbStructure) -> pymongo.ReplaceOne:
        key_filter = self._get_object_key_dict(object)
        object_dict = self._get_cleaned_dict(object)
        return pymongo.ReplaceOne(key_filter, object_dict, True)

    def _get_cleaned_dict(self, object: DbStructure) -> dict[str, Any]:
        object_dict = object.to_dict()
        keys_to_remove = self._get_keys_to_remove(object)

        for key in keys_to_remove:
            object_dict.pop(key)
        return object_dict

    def _get_keys_to_remove(self, object: DbStructure) -> list[str]:
        key_dict = self._get_object_key_dict(object)
        object_dict = object.to_dict()
        keys_to_remove = []

        for key, value in object_dict.items():
            if value is None or value == "" or key in key_dict:
                keys_to_remove.append(key)
        return keys_to_remove

    def _get_object_key_dict(self, object: DbStructure) -> dict[str, dict[str, Any]]:
        key_generic_filter = object.get_key_value()
        key_mongo_filter = MognoDbFilter.create_by_generic(key_generic_filter)
        return key_mongo_filter.translate_for_db()
