from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class MigrationData:
    def __init__(self, **kwargs):
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def create_schema_change_log_table(self) -> Result:
        return self.__connection_manager.query(f"""
            CREATE TABLE IF NOT EXISTS schema_change_log (
                id INT NOT NULL AUTO_INCREMENT,
                file_name VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
            );
        """)

    def run_file(self, file_name: str) -> Result:
        with open(file_name, 'r') as file:
            cmd: str = file.read().strip()
            return self.__connection_manager.query(cmd)
