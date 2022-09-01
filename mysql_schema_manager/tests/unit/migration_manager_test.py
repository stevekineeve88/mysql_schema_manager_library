import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock, Mock
from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.exceptions.change_log_creation_exception import ChangeLogCreationException
from mysql_schema_manager.modules.migration.exceptions.log_fetch_exception import LogFetchException
from mysql_schema_manager.modules.migration.managers.migration_manager import MigrationManager
from mysql_schema_manager.modules.migration.objects.result import Result


class MigrationManagerTest(unittest.TestCase):

    @patch("mysql_schema_manager.modules.migration.data.migration_data")
    def setUp(self, migration_data: MigrationData) -> None:
        self.migration_data: MigrationData = migration_data
        self.root_directory: str = "mysql_schema_manager/tests"
        self.migration_manager: MigrationManager = MigrationManager(
            migration_data=self.migration_data,
            root_directory=self.root_directory
        )

    def test_run_returns_true_result(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        self.migration_data.get_change_logs = MagicMock(return_value=Result(True))
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.migration_data.insert_change_log = MagicMock(return_value=Result(True))

        result = self.migration_manager.run()

        self.migration_data.create_schema_change_log_table.assert_called_once()
        self.migration_data.get_change_logs.assert_called_once()
        self.assertEqual(2, self.migration_data.run_file.call_count)
        self.assertEqual(2, self.migration_data.insert_change_log.call_count)
        self.assertTrue(result.get_status())

    def test_run_skips_used_script(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        self.migration_data.get_change_logs = MagicMock(return_value=Result(True, "", [
            {
                "id": 1,
                "file_name": "test1.sql",
                "timestamp": datetime.now()
            }
        ]))
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.migration_data.insert_change_log = MagicMock(return_value=Result(True))

        self.migration_manager.run()

        self.assertEqual(1, self.migration_data.run_file.call_count)
        self.assertEqual(1, self.migration_data.insert_change_log.call_count)

    def test_run_fails_on_schema_change_log_creation_error(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(False))
        self.migration_data.get_change_logs = MagicMock(return_value=Result(True))
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.migration_data.insert_change_log = MagicMock(return_value=Result(True))

        with self.assertRaises(ChangeLogCreationException):
            self.migration_manager.run()
            self.fail("Did not fail on change log creation error")

        self.migration_data.create_schema_change_log_table.assert_called_once()
        self.migration_data.get_change_logs.assert_not_called()
        self.migration_data.run_file.assert_not_called()
        self.migration_data.insert_change_log.assert_not_called()

    def test_run_fails_on_get_change_logs_error(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        self.migration_data.get_change_logs = MagicMock(return_value=Result(False))
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.migration_data.insert_change_log = MagicMock(return_value=Result(True))

        with self.assertRaises(LogFetchException):
            self.migration_manager.run()
            self.fail("Did not fail on log fetch error")

        self.migration_data.create_schema_change_log_table.assert_called_once()
        self.migration_data.get_change_logs.assert_called_once()
        self.migration_data.run_file.assert_not_called()
        self.migration_data.insert_change_log.assert_not_called()

    def test_run_returns_false_result_with_successful_scripts(self):
        failure_message = "Failed on specific script"
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        self.migration_data.get_change_logs = MagicMock(return_value=Result(True))
        self.migration_data.run_file = Mock()
        self.migration_data.run_file.side_effect = [
            Result(True),
            Result(False, failure_message)
        ]
        self.migration_data.insert_change_log = MagicMock(return_value=Result(True))

        result = self.migration_manager.run()

        self.assertFalse(result.get_status())
        self.assertEqual(f"Error in test2.sql: {failure_message}", result.get_message())
        self.assertListEqual(["test1.sql"], result.get_data())
        self.assertEqual(1, self.migration_data.insert_change_log.call_count)
