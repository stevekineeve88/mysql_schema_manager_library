from typing import List
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class MigrationData:
    """ Data layer for migration operations
    """

    def __init__(self, **kwargs):
        """ Constructor for MigrationData
        Args:
            **kwargs:   Dependencies
                connection_manager (ConnectionManager) - MySQL connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def create_schema_change_log_table(self) -> Result:
        """ Create schema change log table for tracking
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            CREATE TABLE IF NOT EXISTS schema_change_log (
                id INT NOT NULL AUTO_INCREMENT,
                file_name VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
            );
        """)

    def run_file(self, file_name: str) -> Result:
        """ Run SQL script file
        Args:
            file_name (str):        SQL script file with root directory
        Returns:
            Result
        """
        with open(file_name, 'r') as file:
            commands: List[str] = file.read().strip().split(";")
            return self.__connection_manager.query_list(commands)
