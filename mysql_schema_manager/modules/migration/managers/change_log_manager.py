from typing import Dict, List
from mysql_schema_manager.modules.migration.data.change_log_data import ChangeLogData
from mysql_schema_manager.modules.migration.exceptions.change_log_creation_exception import ChangeLogCreationException
from mysql_schema_manager.modules.migration.exceptions.change_log_fetch_exception import ChangeLogFetchException
from mysql_schema_manager.modules.migration.objects.change_log import ChangeLog


class ChangeLogManager:
    def __init__(self, **kwargs):
        self.__change_log_data: ChangeLogData = kwargs.get("change_log_data")

    def create(self, file_name: str) -> ChangeLog:
        result = self.__change_log_data.insert(file_name)
        if not result.get_status():
            raise ChangeLogCreationException(f"Could not create change log entry: {result.get_message()}")
        return self.get_by_id(result.get_last_insert_id())

    def get_by_id(self, change_log_id: int) -> ChangeLog:
        result = self.__change_log_data.load_by_id(change_log_id)
        if result.get_affected_rows() == 0:
            raise ChangeLogFetchException(f"Could not fetch change log entry: {result.get_message()}")
        return self.__build_change_log(result.get_data()[0])

    def get_all(self) -> List[ChangeLog]:
        result = self.__change_log_data.load_all()
        if not result.get_status():
            raise ChangeLogFetchException(f"Could not fetch change log entries: {result.get_message()}")
        data = result.get_data()

        change_logs: List[ChangeLog] = []
        for datum in data:
            change_logs.append(self.__build_change_log(datum))
        return change_logs

    @classmethod
    def __build_change_log(cls, data: Dict[str, any]) -> ChangeLog:
        return ChangeLog(
            data["id"],
            data["file_name"],
            data["timestamp"]
        )
