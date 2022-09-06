from datetime import datetime


class ChangeLog:
    def __init__(self, change_log_id: int, file_name: str, timestamp: datetime):
        self.__id: int = change_log_id
        self.__file_name: str = file_name
        self.__timestamp: datetime = timestamp

    def get_id(self) -> int:
        return self.__id

    def get_file_name(self) -> str:
        return self.__file_name

    def get_timestamp(self) -> datetime:
        return self.__timestamp
