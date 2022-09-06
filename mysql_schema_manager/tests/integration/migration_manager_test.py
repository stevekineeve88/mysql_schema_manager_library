from mysql_schema_manager.tests.integration.setup.integration_setup import IntegrationSetup


class MigrationManagerTest(IntegrationSetup):

    def test_run_runs_migrations_and_returns_result(self):
        change_logs_expected = [
            "test1.sql",
            "test2.sql"
        ]
        tables_expected = [
            "test1",
            "test2"
        ]

        change_logs = self.migration_result.get_change_logs()
        self.assertEqual(2, len(self.migration_result.get_change_logs()))
        for change_log in change_logs:
            self.assertIn(change_log.get_file_name(), change_logs_expected)

        result = self.connection_manager.select(f"""
            SELECT test FROM test2
        """)

        self.assertEqual(1, result.get_affected_rows())
        self.assertEqual("High", result.get_data()[0]["test"])

        result = self.connection_manager.select(f"""
            SELECT 
                TABLE_NAME 
            FROM information_schema.tables 
            WHERE table_schema = 'test_schema'
            AND (
                TABLE_NAME = 'test1'
                OR TABLE_NAME = 'test2'
            )
        """)

        self.assertEqual(2, result.get_affected_rows())
        data = result.get_data()
        for datum in data:
            self.assertIn(datum["TABLE_NAME"], tables_expected)
