import unittest
from dotenv import load_dotenv
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_schema_manager.modules.migration.data.change_log_data import ChangeLogData
from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.managers.change_log_manager import ChangeLogManager
from mysql_schema_manager.modules.migration.managers.migration_manager import MigrationManager
from mysql_schema_manager.modules.migration.objects.migration_result import MigrationResult


class IntegrationSetup(unittest.TestCase):
    connection_manager: ConnectionManager = None
    migration_manager: MigrationManager = None
    change_log_manager: ChangeLogManager = None
    migration_result: MigrationResult = None

    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()

        cls.connection_manager: ConnectionManager = ConnectionManager("my_pool", 3)
        cls.change_log_manager: ChangeLogManager = ChangeLogManager(
            change_log_data=ChangeLogData(
                connection_manager=cls.connection_manager
            )
        )
        cls.migration_manager: MigrationManager = MigrationManager(
            migration_data=MigrationData(
                connection_manager=cls.connection_manager
            ),
            change_log_manager=cls.change_log_manager
        )

        cls.migration_result = cls.migration_manager.run()

    def tearDown(self) -> None:
        result = self.connection_manager.query(f"""
            DELETE FROM schema_change_log WHERE file_name != 'test1.sql' AND file_name != 'test2.sql'
        """)
        if not result.get_status():
            raise Exception(f"Error on teardown instance: {result.get_message()}")

    @classmethod
    def tearDownClass(cls) -> None:
        result = cls.connection_manager.query_list([
            "DROP TABLE IF EXISTS test1",
            "DROP TABLE IF EXISTS test2",
            "DROP TABLE IF EXISTS schema_change_log"
        ])
        if not result.get_status():
            raise Exception(f"Error on teardown class: {result.get_message()}")
