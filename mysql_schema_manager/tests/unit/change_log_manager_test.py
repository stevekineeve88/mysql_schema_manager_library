import unittest
from datetime import datetime
from typing import Dict, List
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from mysql_schema_manager.modules.migration.data.change_log_data import ChangeLogData
from mysql_schema_manager.modules.migration.exceptions.change_log_creation_exception import ChangeLogCreationException
from mysql_schema_manager.modules.migration.exceptions.change_log_fetch_exception import ChangeLogFetchException
from mysql_schema_manager.modules.migration.managers.change_log_manager import ChangeLogManager


class ChangeLogManagerTest(unittest.TestCase):

    @patch("mysql_schema_manager.modules.migration.data.change_log_data")
    def setUp(self, change_log_data: ChangeLogData) -> None:
        self.change_log_data = change_log_data
        self.change_log_manager: ChangeLogManager = ChangeLogManager(
            change_log_data=self.change_log_data
        )

    def test_create_creates_change_log(self):
        insert_id = 1
        file_name = "some_file.sql"
        timestamp = datetime.now()

        insert_result = Result(True)
        insert_result.set_last_insert_id(insert_id)

        select_result = Result(True, "", [{
            "id": insert_id,
            "file_name": file_name,
            "timestamp": timestamp
        }])
        select_result.set_affected_rows(1)

        self.change_log_data.insert = MagicMock(return_value=insert_result)
        self.change_log_data.load_by_id = MagicMock(return_value=select_result)

        change_log = self.change_log_manager.create(file_name)

        self.change_log_data.insert.assert_called_once_with(file_name)
        self.change_log_data.load_by_id.assert_called_once_with(insert_id)
        self.assertEqual(insert_id, change_log.get_id())
        self.assertEqual(file_name, change_log.get_file_name())
        self.assertEqual(timestamp, change_log.get_timestamp())

    def test_create_fails_on_insert_fail(self):
        self.change_log_data.insert = MagicMock(return_value=Result(False))
        self.change_log_data.load_by_id = MagicMock(return_value=Result(True))

        with self.assertRaises(ChangeLogCreationException):
            self.change_log_manager.create("some_file.sql")
            self.fail("Did not fail on change log creation")
        self.change_log_data.insert.assert_called_once()
        self.change_log_data.load_by_id.assert_not_called()

    def test_get_by_id_fails_on_missing_record(self):
        self.change_log_data.load_by_id = MagicMock(return_value=Result(True))

        with self.assertRaises(ChangeLogFetchException):
            self.change_log_manager.get_by_id(1)
            self.fail("Did not fail on change log fetch by ID")
        self.change_log_data.load_by_id.assert_called_once()

    def test_get_all_returns_all_change_logs(self):
        change_log_dicts: List[Dict[str, any]] = [
            {"id": 1, "file_name": "some_file_name.sql", "timestamp": datetime.now()},
            {"id": 2, "file_name": "some_file_name_2.sql", "timestamp": datetime.now()}
        ]
        select_result = Result(True, "", change_log_dicts)
        select_result.set_affected_rows(len(change_log_dicts))

        self.change_log_data.load_all = MagicMock(return_value=select_result)

        change_logs = self.change_log_manager.get_all()

        self.change_log_data.load_all.assert_called_once()

        for i in range(0, len(change_log_dicts)):
            self.assertEqual(change_log_dicts[i]["id"], change_logs[i].get_id())
            self.assertEqual(change_log_dicts[i]["file_name"], change_logs[i].get_file_name())
            self.assertEqual(change_log_dicts[i]["timestamp"], change_logs[i].get_timestamp())

    def test_get_all_fails_on_load_all_fail(self):
        self.change_log_data.load_all = MagicMock(return_value=Result(False))

        with self.assertRaises(ChangeLogFetchException):
            self.change_log_manager.get_all()
            self.fail("Did not fail on change log fetch all")

        self.change_log_data.load_all.assert_called_once()
