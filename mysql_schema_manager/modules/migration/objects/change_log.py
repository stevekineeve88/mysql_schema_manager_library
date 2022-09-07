from datetime import datetime


class ChangeLog:
    """ Object representing a change log
    """
    def __init__(self, change_log_id: int, file_name: str, timestamp: datetime):
        """ Constructor for ChangeLog
        Args:
            change_log_id (int):        Change Log ID
            file_name (str):            Change Log file name without root directory
            timestamp (datetime):       Change Log execution timestamp
        """
        self.__id: int = change_log_id
        self.__file_name: str = file_name
        self.__timestamp: datetime = timestamp

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

    def get_file_name(self) -> str:
        """ Get file name
        Returns:
            str
        """
        return self.__file_name

    def get_timestamp(self) -> datetime:
        """ Get timestamp
        Returns:
            datetime
        """
        return self.__timestamp
