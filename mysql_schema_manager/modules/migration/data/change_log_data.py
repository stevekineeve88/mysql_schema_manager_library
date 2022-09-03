from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class ChangeLogData:
    def __init__(self, **kwargs):
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, file_name: str) -> Result:
        return self.__connection_manager.insert(f"""
            INSERT INTO schema_change_log (file_name) VALUES (%(file_name)s)
        """, {
            "file_name": file_name
        })

    def load_by_id(self, change_log_id: int) -> Result:
        return self.__connection_manager.select(f"""
            SELECT
                schema_change_log.id,
                schema_change_log.file_name,
                schema_change_log.timestamp 
            FROM schema_change_log
            WHERE schema_change_log.id = %(id)s
        """, {
            "id": change_log_id
        })

    def load_all(self) -> Result:
        return self.__connection_manager.select(f"""
            SELECT
                schema_change_log.id,
                schema_change_log.file_name,
                schema_change_log.timestamp 
            FROM schema_change_log
        """)
