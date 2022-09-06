from mysql_schema_manager.tests.integration.setup.integration_setup import IntegrationSetup


class ChangeLogManagerTest(IntegrationSetup):

    def test_create_creates_change_log(self):
        file_name = "create_log_test.sql"
        created_change_log = self.change_log_manager.create(file_name)
        fetch_change_log = self.change_log_manager.get_by_id(created_change_log.get_id())

        self.assertEqual(created_change_log.get_id(), fetch_change_log.get_id())
        self.assertEqual(created_change_log.get_file_name(), fetch_change_log.get_file_name())
        self.assertEqual(created_change_log.get_timestamp(), fetch_change_log.get_timestamp())

    def test_get_all_gets_all_change_logs(self):
        change_logs = self.change_log_manager.get_all()

        file_names = [
            "test1.sql",
            "test2.sql"
        ]

        self.assertEqual(2, len(change_logs))
        for change_log in change_logs:
            self.assertIn(change_log.get_file_name(), file_names)
