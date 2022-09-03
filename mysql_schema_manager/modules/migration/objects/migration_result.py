from typing import List

from mysql_schema_manager.modules.migration.objects.change_log import ChangeLog


class MigrationResult:
    def __init__(self, status: bool, message: str = "", change_logs: List[ChangeLog] = []):
        self.__status: bool = status
        self.__message: str = message
        self.__change_logs: List[ChangeLog] = change_logs

    def get_status(self) -> bool:
        return self.__status

    def get_message(self) -> str:
        return self.__message

    def get_change_logs(self) -> List[ChangeLog]:
        return self.__change_logs
