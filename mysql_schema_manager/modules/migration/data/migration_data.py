import os
import mysql.connector
from mysql_schema_manager.modules.migration.objects.result import Result


class MigrationData:
    def __init__(self, **kwargs):
        self.__host = kwargs.get("host") or os.environ["DB_MIGRATION_HOST"]
        self.__port = kwargs.get("port") or os.environ["DB_MIGRATION_PORT"]
        self.__user = kwargs.get("user") or os.environ["DB_MIGRATION_USERNAME"]
        self.__pwd = kwargs.get("pwd") or os.environ["DB_MIGRATION_PWD"]
        self.__db = kwargs.get("db") or os.environ["DB_MIGRATION_DB"]

        self.__connection = mysql.connector.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__pwd,
            database=self.__db
        )

    def create_schema_change_log_table(self) -> Result:
        cursor = self.__connection.cursor()
        try:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS schema_change_log (
                    id INT NOT NULL AUTO_INCREMENT,
                    file_name VARCHAR(255) NOT NULL,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`));
                """)
            return Result(True)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()

    def insert_change_log(self, file_name: str) -> Result:
        cursor = self.__connection.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO schema_change_log (file_name) VALUES (?)
            """, file_name)
            return Result(True)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()

    def get_change_logs(self):
        cursor = self.__connection.cursor(dictionary=True)
        try:
            cursor.execute(f"""
                SELECT
                    id,
                    file_name,
                    timestamp 
                FROM schema_change_log
            """)
            rows = cursor.fetchall()
            return Result(True, "", rows)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()

    def run_file(self, file_name: str) -> Result:
        cursor = self.__connection.cursor()
        try:
            with open(file_name, 'r') as file:
                cmd: str = file.read().strip()
                cursor.execute(cmd)
            return Result(True)
        except Exception as e:
            return Result(False, str(e))
        finally:
            cursor.close()
