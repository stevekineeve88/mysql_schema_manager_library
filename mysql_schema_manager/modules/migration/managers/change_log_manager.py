from typing import Dict, List
from mysql_schema_manager.modules.migration.data.change_log_data import ChangeLogData
from mysql_schema_manager.modules.migration.exceptions.change_log_creation_exception import ChangeLogCreationException
from mysql_schema_manager.modules.migration.exceptions.change_log_fetch_exception import ChangeLogFetchException
from mysql_schema_manager.modules.migration.objects.change_log import ChangeLog


class ChangeLogManager:
    """ Manager for managing change log objects
    """
    def __init__(self, **kwargs):
        """ Constructor for ChangeLogManager
        Args:
            **kwargs: Dependencies
                change_log_data (ChangeLogData) - Change log data layer
        """
        self.__change_log_data: ChangeLogData = kwargs.get("change_log_data")

    def create(self, file_name: str) -> ChangeLog:
        """ Create change log
        Args:
            file_name (str):    SQL script file name without root directory
        Returns:
            ChangeLog
        """
        result = self.__change_log_data.insert(file_name)
        if not result.get_status():
            raise ChangeLogCreationException(f"Could not create change log entry: {result.get_message()}")
        return self.get_by_id(result.get_last_insert_id())

    def get_by_id(self, change_log_id: int) -> ChangeLog:
        """ Get change log by ID
        Args:
            change_log_id (int):
        Returns:
            ChangeLog
        """
        result = self.__change_log_data.load_by_id(change_log_id)
        if result.get_affected_rows() == 0:
            raise ChangeLogFetchException(f"Could not fetch change log entry: {result.get_message()}")
        return self.__build_change_log(result.get_data()[0])

    def get_all(self) -> List[ChangeLog]:
        """ Get all change logs
        Returns:
            List[ChangeLog]
        """
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
        """ Build change log object
        Args:
            data (Dict[str, any]):      Dict representation of change log
        Returns:
            ChangeLog
        """
        return ChangeLog(
            data["id"],
            data["file_name"],
            data["timestamp"]
        )
