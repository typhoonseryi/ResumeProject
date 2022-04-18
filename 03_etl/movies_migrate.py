import argparse
import os
import sys
import time
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor

from connect_helpers import backoff, connect_db
from es_handler import ESSaver
from logging_settings import logger
from postgres_handler import PostgresLoader
from state_storage import ShelveStorage, State


@backoff()
def migrate_data(
    table_name: str,
    chunk_size: int,
    state_key: str,
    search_period: int,
    state_filename: str,
    pg_dsl: dict,
    es_dsl: dict,
) -> None:
    """Функция переноса обновленных данных из БД Postgres в ElasticSearch"""
    shelve_storage = ShelveStorage(state_filename)
    state_storage = State(shelve_storage)

    while True:
        modified_dt = state_storage.get_state(state_key)
        if modified_dt is None:
            modified_dt = datetime.min

        with connect_db(
            **pg_dsl, cursor_factory=DictCursor, func=psycopg2.connect
        ) as pg_conn:
            logger.info("+ Succesfully connected to postgres")

            es_conn = Elasticsearch([es_dsl])
            logger.info("+ Succesfully connected to ES")

            es_saver = ESSaver(es_conn, state_storage, state_key)

            postgres_loader = PostgresLoader(
                pg_conn, es_saver, table_name, modified_dt, chunk_size
            )
            postgres_loader.save_table_data()
        time.sleep(search_period)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", default="film_work")
    parser.add_argument("-c", "--chunk-size", default=100)
    parser.add_argument("-s", "--search-period", default=60)
    parser.add_argument("-f", "--state-filename", default="state_file")
    namespace = parser.parse_args(sys.argv[1:])

    options = {
        "table_name": namespace.table,
        "chunk_size": int(namespace.chunk_size),
        "state_key": "modified_" + namespace.table,
        "search_period": int(namespace.search_period),
        "state_filename": namespace.state_filename,
    }

    load_dotenv()
    pg_dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
    }
    es_dsl = {
        "host": os.environ.get("ES_HOST", "localhost"),
        "port": os.environ.get("ES_PORT", 9200),
    }
    options["pg_dsl"] = pg_dsl
    options["es_dsl"] = es_dsl

    migrate_data(**options)


if __name__ == "__main__":
    main()
