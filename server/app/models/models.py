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
            ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;
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


class Applicant(BaseModel):
    table_name = "applicant"
    indexes = {}
    table_creation_statement = """
        create table applicant
            (
              email          varchar(320)                        not null
                primary key,
              password       varchar(320)                        not null,
              applicant_name varchar(13)                         null,
              sex            enum ('MALE', 'FEMALE')             null,
              birth_date     date                                null,
              parent_name    varchar(13)                         null,
              parent_tel     varchar(12)                         null,
              applicant_tel  varchar(12)                         null,
              address        varchar(500)                        null,
              post_code      varchar(5)                          null,
              image_path     varchar(256)                        null,
              created_at     timestamp default CURRENT_TIMESTAMP not null,
              updated_at     timestamp default CURRENT_TIMESTAMP not null,
              constraint applicant_tel_UNIQUE
              unique (applicant_tel),
              constraint image_path_UNIQUE
              unique (image_path)
            ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ;
    """

    email = Email()
    password = Password()
    applicant_name = String(length=13)
    sex = SexEnum()
    birth_date = Date()
    parent_tel = PhoneNumber()
    applicant_tel = PhoneNumber()
    address = String(500)
    post_code = String(5, regex=r"[0-9]{5}")
    image_path = String(256)
    created_at = TimeStamp(default=datetime.datetime.now)
    updated_at = TimeStamp(default=created_at)

    def save(self):
        query = f"""INSERT INTO {self.table_name} ( 
                    email,
                    password,
                    applicant_name,
                    sex,
                    birth_date,
                    parent_tel,
                    applicant_tel,
                    address,
                    post_code,
                    image_path,
                    created_at,
                    updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        MySQLConnection.execute(query, self.email, self.password, self.applicant_name, self.sex,
                                self.birth_date, self.parent_tel, self.applicant_tel, self.address, self.post_code,
                                self.image_path, self.created_at, self.updated_at)
