import os
from sqlite3 import dbapi2
from jaguarundi.config import PATH_TO_DB, FULL_PATH_TO_DB, FOREIGN_KEYS_CONTROL, PRINT_REQUESTS

if not os.path.isdir(PATH_TO_DB):
    raise NotADirectoryError(f'Error: directory {PATH_TO_DB} does not exist')

if not os.access(PATH_TO_DB, os.W_OK):
    raise Exception(f'Error: directory {PATH_TO_DB} does is not writable')


def connect_to_db(path: str = FULL_PATH_TO_DB) -> dbapi2:
    """Connects to the default database."""
    connection = dbapi2.connect(path)
    if FOREIGN_KEYS_CONTROL:
        connection.cursor().execute('PRAGMA foreign_keys = ON;')
    return connection


def print_raw_request(request: str) -> None:
    if PRINT_REQUESTS:
        print(request)


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
