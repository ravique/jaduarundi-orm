import os
from sqlite3 import dbapi2
from .config import DB_NAME

# TODO: Write errors

db_path = os.path.join(os.getcwd(), DB_NAME)


def connect_to_db(path: str = db_path):
    """Connects to the default database."""
    connection = dbapi2.connect(path)
    return connection


def get_data_from_kwargs(**kwargs):
    fields = ', '.join(kwargs.keys())
    values = ', '.join([repr(v) if isinstance(v, str) else str(v) for v in kwargs.values()])
    return fields, values