from typing import List


class Result:
    def __init__(self, status: bool, message: str = "", data: List[any] = []):
        self.__status: bool = status
        self.__message: str = message
        self.__data: List[any] = data

    def get_status(self) -> bool:
        return self.__status

    def get_message(self) -> str:
        return self.__message

    def get_data(self) -> List[any]:
        return self.__data
