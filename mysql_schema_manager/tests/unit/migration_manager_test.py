import os
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock, Mock

from mysql_data_manager.modules.connection.objects.result import Result

from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.exceptions.change_log_table_creation_exception import \
    ChangeLogTableCreationException
from mysql_schema_manager.modules.migration.managers.change_log_manager import ChangeLogManager
from mysql_schema_manager.modules.migration.managers.migration_manager import MigrationManager
from mysql_schema_manager.modules.migration.objects.change_log import ChangeLog


class MigrationManagerTest(unittest.TestCase):

    @patch("mysql_schema_manager.modules.migration.data.migration_data")
    @patch("mysql_schema_manager.modules.migration.managers.change_log_manager")
    def setUp(self, migration_data: MigrationData, change_log_manager: ChangeLogManager) -> None:
        self.migration_data: MigrationData = migration_data
        self.change_log_manager: ChangeLogManager = change_log_manager
        self.root_directory: str = "mysql_schema_manager/tests"
        self.migration_manager: MigrationManager = MigrationManager(
            migration_data=self.migration_data,
            change_log_manager=self.change_log_manager,
            root_directory=self.root_directory
        )
        self.created_files = []

    def test_run_returns_true_result(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        self.change_log_manager.get_all = MagicMock(return_value=[])
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.change_log_manager.create = Mock()
        self.change_log_manager.create.side_effect = [
            ChangeLog(1, "some_script.sql", datetime.now()),
            ChangeLog(2, "some_script.sql", datetime.now())
        ]

        result = self.migration_manager.run()

        self.migration_data.create_schema_change_log_table.assert_called_once()
        self.change_log_manager.get_all.assert_called_once()
        self.assertEqual(2, self.migration_data.run_file.call_count)
        self.assertEqual(2, self.change_log_manager.create.call_count)
        self.assertTrue(result.get_status())

    def test_run_skips_used_script(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        ChangeLog(1, "test1.sql", datetime.now())
        self.change_log_manager.get_all = MagicMock(return_value=[ChangeLog(1, "test1.sql", datetime.now())])
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.change_log_manager.create = MagicMock(return_value=ChangeLog(2, "test2.sql", datetime.now()))

        self.migration_manager.run()

        self.migration_data.run_file.assert_called_once_with(f"{self.root_directory}/scripts/test2.sql")
        self.change_log_manager.create.assert_called_once_with("test2.sql")

    def test_run_fails_on_schema_change_log_creation_error(self):
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(False))
        self.change_log_manager.get_all = MagicMock(return_value=[])
        self.migration_data.run_file = MagicMock(return_value=Result(True))
        self.change_log_manager.create = MagicMock(return_value=ChangeLog(1, "some_script.sql", datetime.now()))

        with self.assertRaises(ChangeLogTableCreationException):
            self.migration_manager.run()
            self.fail("Did not fail on change log creation error")

        self.migration_data.create_schema_change_log_table.assert_called_once()
        self.change_log_manager.get_all.assert_not_called()
        self.migration_data.run_file.assert_not_called()
        self.change_log_manager.create.assert_not_called()

    def test_run_returns_false_result_with_successful_scripts(self):
        failure_message = "Failed on specific script"
        self.migration_data.create_schema_change_log_table = MagicMock(return_value=Result(True))
        self.change_log_manager.get_all = MagicMock(return_value=[])
        self.migration_data.run_file = Mock()
        self.migration_data.run_file.side_effect = [
            Result(True),
            Result(False, failure_message)
        ]
        self.change_log_manager.create = MagicMock(return_value=ChangeLog(1, "test1.sql", datetime.now()))

        result = self.migration_manager.run()

        self.assertFalse(result.get_status())
        self.assertEqual(f"Error in test2.sql: {failure_message}", result.get_message())
        self.assertEqual("test1.sql", result.get_change_logs()[0].get_file_name())
        self.assertEqual(1, self.change_log_manager.create.call_count)

    def test_generate_file_generates_sql_file_with_datetime(self):
        file_name = self.__generate_file()
        with open(f"{self.root_directory}/scripts/{file_name}", "r") as file:
            lines = file.readlines()
            self.assertEqual(1, len(lines))
            self.assertEqual(f"-- Generated SQL file - {file_name.split('.')[0]}", lines[0])

    def tearDown(self) -> None:
        for created_file in self.created_files:
            os.remove(f"{self.root_directory}/scripts/{created_file}")

    def __generate_file(self) -> str:
        file_name = self.migration_manager.generate_file()
        self.created_files.append(file_name)
        return file_name

