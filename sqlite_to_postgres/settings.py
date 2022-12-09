import os

POSTGRES_CONNECTION_SETTINGS = {
    "dbname": os.environ.get("PG_DB_NAME"),
    "user": os.environ.get("PG_DB_USER"),
    "password": os.environ.get("PG_DB_PASSWORD"),
    "host": os.environ.get("PG_DB_HOST"),
    "port": os.environ.get("PG_DB_PORT"),
}

SQLITE_DB_FILE = os.environ.get("SQLITE_DB_FILE")