import datetime
import uuid
from typing import Dict, Union, Iterable, Tuple, List

from server.app.models.connection import MySQLConnection
from server.app.models.descriptor import *


class BaseModel:
    table_name: str
    indexes: Dict[str, Union[str, Tuple]]

    table_creation_statement: str

    @classmethod
    def create_table(cls):
        MySQLConnection.execute(cls.table_creation_statement)
        cls.create_table_index()

    @classmethod
    def create_table_index(cls):
        for index_name, index_key in cls.indexes.items():
            MySQLConnection.execute(f"CREATE INDEX {index_name} ON {cls.table_name} ({', '.join(str(i) for i in index_key)})")

    def save(self):
        pass


class Admin(BaseModel):
    table_name = "admin"
    indexes = {
        "type_index": ("admin_type", )
    }

    table_creation_statement = """
        create table if not exists admin
            (
              admin_id       varchar(45)                                  not null
                primary key,
              admin_password varchar(320)                                  not null,
              admin_type     enum ('ROOT', 'ADMINISTRATION', 'INTERVIEW') not null,
              admin_email    varchar(320)                                 not null,
              admin_name     varchar(13)                                  not null,
              created_at     timestamp default CURRENT_TIMESTAMP          not null,
              updated_at     timestamp default CURRENT_TIMESTAMP          not null
            );
    """

    admin_id = UUID()
    admin_password = Password()
    admin_type = AdminEnum()
    admin_email = Email()
    admin_name = String(length=13)
    created_at = TimeStamp(default=datetime.datetime.now)
    updated_at = TimeStamp(default=created_at)

    def __init__(self, admin_name, admin_email, admin_password, admin_type, admin_id=None, created_at=None, updated_at=None):
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.admin_type = admin_type

        if created_at and updated_at and admin_id:
            self.admin_id = admin_id
            self.created_at = created_at
            self.updated_at = updated_at

    def save(self):
        query = f"""INSERT INTO {self.table_name} (
                    admin_id,
                    admin_password,
                    admin_type,
                    admin_email,
                    admin_name,
                    created_at,
                    updated_at,
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        MySQLConnection.execute(query, self.admin_id, self.admin_password,
                                self.admin_type, self.admin_email, self.admin_name,
                                self.created_at, self.updated_at)

