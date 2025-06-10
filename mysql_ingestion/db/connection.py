import mysql.connector


class Connection:
    def __init__(
        self, host: str, port: int, user: str, password: str, database: str
    ) -> None:
        self.__config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }

    def get_connection(self):
        return mysql.connector.connect(**self.__config)
