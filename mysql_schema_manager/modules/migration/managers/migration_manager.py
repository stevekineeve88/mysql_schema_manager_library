import os
from os.path import isfile, join
from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.exceptions.change_log_creation_exception import ChangeLogCreationException
from mysql_schema_manager.modules.migration.exceptions.log_fetch_exception import LogFetchException
from mysql_schema_manager.modules.migration.objects.result import Result


class MigrationManager:
    def __init__(self, **kwargs):
        self.__migration_data: MigrationData = kwargs.get("migration_data") or MigrationData()
        self.__root_directory: str = kwargs.get("root_directory") or os.environ["DB_MIGRATION_ROOT_DIR"]
        self.__script_directory: str = f"{self.__root_directory}/scripts"

    def run(self) -> Result:
        result = self.__migration_data.create_schema_change_log_table()
        if not result.get_status():
            raise ChangeLogCreationException(result.get_message())

        result = self.__migration_data.get_change_logs()
        if not result.get_status():
            raise LogFetchException(result.get_message())

        logs = result.get_data()
        scripts = [f for f in os.listdir(self.__script_directory) if isfile(join(self.__script_directory, f))]
        scripts = sorted(scripts)

        used_scripts = [log["file_name"] for log in logs]
        unused_scripts = list(set(scripts) - set(used_scripts))
        unused_scripts = sorted(unused_scripts)

        completed = []
        for script in unused_scripts:
            result = self.__migration_data.run_file(f"{self.__script_directory}/{script}")
            if not result.get_status():
                return Result(False, f"Error in {script}: {result.get_message()}", completed)
            self.__migration_data.insert_change_log(script)
            completed.append(script)
        return Result(True, "", completed)

