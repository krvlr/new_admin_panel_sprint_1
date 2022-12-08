import logging
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, astuple, dataclass

import psycopg2
from dotenv import load_dotenv
from psycopg2.errors import Error
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_values

from models_dataclasses import TABLE_NAME_DATACLASS_MAPPING

load_dotenv()


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class SQLiteExtractor:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def extract_table(self, table_name: str) -> list[dataclass]:
        data_class = TABLE_NAME_DATACLASS_MAPPING[table_name]
        curs = self.conn.cursor()
        curs.execute(f"SELECT * FROM {table_name};")
        table_data_list = curs.fetchall()
        return [
            data_class.from_dict(dict(table_line)) for table_line in table_data_list
        ]


class PostgresSaver:
    def __init__(self, conn: _connection) -> None:
        self.conn = conn

    def save_all_data(self, table_name: str, data_list: list[dataclass]):
        curs = self.conn.cursor()

        insert_query = (
            "INSERT INTO content.{0} ({1}) VALUES %s ON CONFLICT (id) DO NOTHING;"
        )

        fields = ", ".join(
            TABLE_NAME_DATACLASS_MAPPING[table_name].__annotations__.keys()
        )

        try:
            execute_values(
                cur=curs,
                sql=insert_query.format(table_name, fields),
                argslist=[astuple(data_row) for data_row in data_list],
            )
            self.conn.commit()
        except (Error, Exception) as e:
            logging.error(f"Ошибка при сохранении в таблицу {table_name}", e)


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    postgres_saver = PostgresSaver(pg_conn)

    for table_name in TABLE_NAME_DATACLASS_MAPPING.keys():
        data = sqlite_extractor.extract_table(table_name)
        postgres_saver.save_all_data(table_name, data)


if __name__ == "__main__":
    dsl = {
        "dbname": os.environ.get("PG_DB_NAME"),
        "user": os.environ.get("PG_DB_USER"),
        "password": os.environ.get("PG_DB_PASSWORD"),
        "host": os.environ.get("PG_DB_HOST"),
        "port": os.environ.get("PG_DB_PORT"),
    }

    with conn_context(
        os.environ.get("SQLITE_DB_FILE")
    ) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
