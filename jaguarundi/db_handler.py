import os
from sqlite3 import dbapi2
from .config import PATH_TO_DB, FOREIGN_KEYS_CONTROL


def connect_to_db(path: str = PATH_TO_DB) -> object:
    """Connects to the default database."""
    connection = dbapi2.connect(path)
    if FOREIGN_KEYS_CONTROL:
        connection.cursor().execute('PRAGMA foreign_keys = ON;')
    return connection


def sql_value_formatter(value: str) -> str:
    if not value:
        return 'null'
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, int):
        return str(value)


def sql_fields_values_formatter(**kwargs):
    fields = ', '.join(kwargs.keys())
    values = ', '.join([sql_value_formatter(value) for value in kwargs.values()])
    return fields, values


def sql_params_formatter(params_dict: dict) -> str:
    return ', '.join(
        ['='.join((str(field), sql_value_formatter(value))) for field, value in params_dict.items()]
    )
