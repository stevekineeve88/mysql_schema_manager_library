from typing import List

from mysql_schema_manager.modules.migration.objects.change_log import ChangeLog


class MigrationResult:
    """ Object representing migration result
    """
    def __init__(self, status: bool, message: str = "", change_logs: List[ChangeLog] = []):
        """ Constructor for MigrationResult
        Args:
            status (bool):                      Status of migration result success
            message (str):                      Error message
            change_logs (List[ChangeLog]):      List of ChangeLog objects for migration result
        """
        self.__status: bool = status
        self.__message: str = message
        self.__change_logs: List[ChangeLog] = change_logs

    def get_status(self) -> bool:
        """ Get status
        Returns:
            bool
        """
        return self.__status

    def get_message(self) -> str:
        """ Get error message
        Returns:
            str
        """
        return self.__message

    def get_change_logs(self) -> List[ChangeLog]:
        """ Get change logs
        Returns:
            List[ChangeLog]
        """
        return self.__change_logs
