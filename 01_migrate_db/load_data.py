import os
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from typing import Any, Generator, List, Tuple, Type

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch, register_uuid

from settings import CHUNK_SIZE, tuple_options
from tables_dataclass import tuple_tables


class PostgresSaver:
    """Класс сохранения данных в БД Postgres"""

    def __init__(self, connection: _connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def save_batch_data(self, batch_list: List[Tuple], options: Tuple[str]):
        """Метод записи некоторого числа строк в таблицу БД"""
        data = list(map(asdict, batch_list))
        query = (
            "INSERT INTO {2}.{3} ({1}) VALUES ({0}) ON CONFLICT (id) DO NOTHING".format(
                *options
            )
        )
        execute_batch(self.cursor, query, data)

    def commit_connection(self):
        self.connection.commit()


class SQLiteLoader:
    """Класс загрузчика данных из БД SQLite"""

    def __init__(self, connection: sqlite3.Connection, target_db: PostgresSaver):
        self.connection = connection
        self.cursor = connection.cursor()
        self.target_db = target_db
        register_uuid()

    def load_batch_data(
        self, table: Type, options: Tuple[str]
    ) -> Generator[List[Tuple], None, None]:
        """Метод загрузки некоторого количества строк из таблицы БД"""
        self.cursor.execute("SELECT * FROM {0}".format(options[3]))
        while True:
            qs_batch = self.cursor.fetchmany(CHUNK_SIZE)
            batch_list = []
            if qs_batch:
                for record in qs_batch:
                    record = table(*record)
                    batch_list.append(record)
            else:
                return
            yield batch_list

    def save_table(self, table: Type, options: Tuple[str]):
        """Метод записи загруженных данных из одной таблицы в другую БД"""
        for batch_list in self.load_batch_data(table, options):
            self.target_db.save_batch_data(batch_list, options)

    def save_all_tables(self):
        """Метод записи загруженных данных из всех таблиц в другую БД"""
        for (table, options) in zip(tuple_tables, tuple_options):
            self.save_table(table, options)
        self.target_db.commit_connection()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection, postgres_saver)

    sqlite_loader.save_all_tables()


@contextmanager
def connect_db(*args: Any, func: Any = sqlite3.connect, **kwargs: Any):
    """Метод подключения к базе данных с использованием декоратора контекстного менеджера"""
    conn = func(*args, **kwargs)
    yield conn
    conn.close()


if __name__ == "__main__":
    load_dotenv()
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
    }
    with connect_db("db.sqlite", func=sqlite3.connect) as sqlite_conn, connect_db(
        **dsl, cursor_factory=DictCursor, func=psycopg2.connect
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
