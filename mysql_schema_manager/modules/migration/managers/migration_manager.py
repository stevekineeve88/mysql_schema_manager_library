import os
from os.path import isfile, join
from typing import List
from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.exceptions.change_log_table_creation_exception import \
    ChangeLogTableCreationException
from mysql_schema_manager.modules.migration.managers.change_log_manager import ChangeLogManager
from mysql_schema_manager.modules.migration.objects.change_log import ChangeLog
from mysql_schema_manager.modules.migration.objects.migration_result import MigrationResult


class MigrationManager:
    def __init__(self, **kwargs):
        self.__migration_data: MigrationData = kwargs.get("migration_data")
        self.__change_log_manager: ChangeLogManager = kwargs.get("change_log_manager")
        self.__root_directory: str = kwargs.get("root_directory") or os.environ["DB_MIGRATION_ROOT_DIR"]
        self.__script_directory: str = f"{self.__root_directory}/scripts"

    def run(self) -> MigrationResult:
        result = self.__migration_data.create_schema_change_log_table()
        if not result.get_status():
            raise ChangeLogTableCreationException(result.get_message())

        logs = self.__change_log_manager.get_all()
        scripts = sorted([f for f in os.listdir(self.__script_directory) if isfile(join(self.__script_directory, f))])

        used_scripts = [log.get_file_name() for log in logs]
        unused_scripts = sorted(list(set(scripts) - set(used_scripts)))

        completed: List[ChangeLog] = []
        for script in unused_scripts:
            result = self.__migration_data.run_file(f"{self.__script_directory}/{script}")
            if not result.get_status():
                return MigrationResult(False, f"Error in {script}: {result.get_message()}", completed)
            completed.append(self.__change_log_manager.create(script))
        return MigrationResult(True, "", completed)

