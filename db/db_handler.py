import os
from sqlite3 import dbapi2
from .config import DB_NAME, FOREIGN_KEYS_CONTROL

db_path = os.path.join(os.getcwd(), DB_NAME)


def connect_to_db(path: str = db_path) -> object:
    """Connects to the default database."""
    connection = dbapi2.connect(path)
    if FOREIGN_KEYS_CONTROL:
        connection.cursor().execute('PRAGMA foreign_keys = ON;')
    return connection


def sql_value_formater(value: str) -> str:
    if not value:
        return 'null'
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, int):
        return str(value)


def sql_fields_values_formatter(**kwargs):
    fields = ', '.join(kwargs.keys())
    values = ', '.join([sql_value_formater(value) for value in kwargs.values()])
    return fields, values


def sql_params_formatter(params_dict: dict) -> str:
    return ', '.join(
        ['='.join((str(field), sql_value_formater(value))) for field, value in params_dict.items()]
    )
