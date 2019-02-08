import datetime
from typing import Dict, Union, Iterable, Tuple, List

from server.app.models.connection import MySQLConnection


class BaseModel:
    table_name: str
    indexes: Dict[str, Union[str, Tuple]]

    @classmethod
    def create_table(cls):
        pass

    @classmethod
    def create_table_index(cls):
        for index_name, index_key in cls.indexes.items():
            MySQLConnection.execute(f"CREATE INDEX {index_name} ON {cls.table_name} ({', '.join(str(i) for i in index_key)})")

    def save(self):
        pass
