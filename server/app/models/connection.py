import pymysql.cursors
import os

CONNECTION_INFO = {
    "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
    "port": os.environ.get("MYSQL_PORT", 3306),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "db": os.environ.get("MYSQL_DATABASE", "entrydsm"),
    "charset": "utf8mb4",
    "use_unicode": True
}  # TODO: os env  --> vault


class MySQLConnection:
    """
    Singleton object for use database
    """
    connection: pymysql.connections.Connection

    @classmethod
    def initialize(cls, connection_info: dict):
        if not connection_info:
            connection_info = CONNECTION_INFO

        cls.connection = pymysql.connect(**connection_info)

    @classmethod
    def destroy(cls):
        cls.connection.close()

    @classmethod
    def execute(cls, query, *args):
        cursor: pymysql.cursors.DictCursor

        with cls.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, args)
            cls.connection.commit()

    @classmethod
    def executemany(cls, query, args):
        cursor: pymysql.cursors.DictCursor

        with cls.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.executemany(query, args)
            cls.connection.commit()

    @classmethod
    def fetch(cls, query, *args):
        cursor: pymysql.cursors.DictCursor

        with cls.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, args)
            cls.connection.commit()
            return cursor.fetchall()

    @classmethod
    def fetchone(cls, query, *args):
        cursor: pymysql.cursors.DictCursor

        with cls.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, args)
            cls.connection.commit()
            return cursor.fetchone()

