from sqlite3 import OperationalError, IntegrityError, Row
from typing import List
from collections import OrderedDict

from .config import *
from .db_handler import connect_to_db, get_data_from_kwargs


def print_raw_request(request):
    if PRINT_REQESTS:
        print(request)


class Field:
    def __init__(self, name: str = None, field_type: str = None, is_null: bool = False, pk: bool = False,
                 auto_increment: bool = False, foreign_key: str = None):
        if name:
            self.name = name
        if not field_type and not foreign_key:
            raise TypeError('Can not create field without type')
        self.type = field_type
        if not is_null:
            self.null = 'NOT NULL'
        if pk:
            self.pk = 'PRIMARY KEY'
        if auto_increment:
            self.auto_increment = 'AUTOINCREMENT'
        if foreign_key:
            self.foreign_key = foreign_key


class Model:
    id = Field(field_type='INTEGER', is_null=False, pk=True, auto_increment=True)  # default PK field

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def __check_fk(cls, connection):
        pre_request = f'PRAGMA foreign_key_list({cls.__get_table_name()});'
        resp = connection.cursor().execute(pre_request).fetchall()
        foreign_keys = []
        if not resp:
            return None

        for row in resp:
            foreign_keys.append(dict(row))

        return foreign_keys

    @classmethod
    def __get_fields(cls):
        fields = {field_name: value for field_name, value in cls.__dict__.items() if
                  not field_name.startswith('__')}
        fields['id'] = cls.id
        return fields

    @classmethod
    def __get_table_name(cls):
        return '_'.join((cls.__name__.lower(), 'tbl'))

    @classmethod
    def __get_fk(cls):
        return f'{cls.__get_table_name()}(id)'

    @classmethod
    def create_table(cls):
        """
        Creates table. If field has param 'name' -> field name == 'name', else field name = object name
        """

        connection = connect_to_db()

        fields = []
        foreign_keys = []

        for field_name, field_params in cls.__get_fields().items():
            field_params_dict = OrderedDict(field_params.__dict__)

            if 'name' not in field_params_dict.keys():
                field_params_dict['name'] = field_name
                field_params_dict.move_to_end('name', last=False)

            if 'foreign_key' in field_params_dict.keys():
                fk_table = field_params_dict.pop('foreign_key')
                field = [value for value in field_params_dict.values() if value]
                foreign_keys.append(f'FOREIGN KEY({field_params_dict["name"]}) REFERENCES {fk_table}')
                # connection.cursor().execute('PRAGMA foreign_keys = ON;')  # TODO: Разобраться что за хрень

            else:
                field = [value for value in field_params_dict.values() if value]
            fields.append(' '.join(field))

        fields += foreign_keys

        request = f'CREATE TABLE {cls.__get_table_name()} ({", ".join(fields)});'
        print_raw_request(request)
        try:
            connection.cursor().execute(request)
        except OperationalError as e:
            print('Unable to create table: ' + str(e))

    @classmethod
    def drop_table(cls):
        connection = connect_to_db()

        request = f'DROP TABLE {cls.__get_table_name()};'
        print_raw_request(request)
        try:
            connection.cursor().execute(request)
        except OperationalError as e:
            print('Unable to drop table: ' + str(e))

    @classmethod
    def create(cls, **kwargs):
        fields, values = get_data_from_kwargs(**kwargs)

        connection = connect_to_db()
        request = f'INSERT INTO {cls.__get_table_name()}({fields}) VALUES({values});'
        print_raw_request(request)

        try:
            connection.cursor().execute(request)
            connection.commit()
        except IntegrityError as e:
            print('Unable to create table: ' + str(e))

    @classmethod
    def __db_getter(cls, **kwargs):

        # TODO: Return error if more than one rows get

        only_fields = ', '.join(kwargs.get('only', '*'))
        kwargs.pop('only', None)

        request_type = kwargs.get('request_type')
        kwargs.pop('request_type', None)

        connection = connect_to_db()
        connection.row_factory = Row

        foreign_keys = cls.__check_fk(connection)

        if foreign_keys:

            to_tables = [t['table'] for t in foreign_keys]
            from_table = cls.__get_table_name()

            from_fields = [t['from'] for t in foreign_keys]
            froms = ['.'.join(i) for i in list(zip([from_table] * len(from_fields), from_fields))]

            to_fields = [i['to'] for i in foreign_keys]
            tos = ['.'.join(i) for i in list(zip(to_tables, to_fields))]

            joins = f'{from_table}'

            for x in range(len(to_tables)):
                joins += f' LEFT JOIN {to_tables[x]} ON {froms[x]}={tos[x]}'

        if request_type == 'all':

            if foreign_keys:
                request = f'SELECT {only_fields} FROM {joins};'
            else:
                request = f'SELECT {only_fields} FROM {cls.__get_table_name()};'

        else:

            conditions = ' AND '.join(
                ['='.join((str(k), repr(v) if isinstance(v, str) else str(v))) for k, v in kwargs.items()]
            )

            if foreign_keys:
                request = f'SELECT {only_fields} FROM {joins} WHERE {conditions};'
            else:
                request = f'SELECT {only_fields} FROM {cls.__get_table_name()} WHERE {conditions};'

        print_raw_request(request)

        if request_type == 'one':
            try:
                row = connection.cursor().execute(request).fetchone()
            except OperationalError as e:
                print('Unable to get: ' + str(e))
                return None

            if row:
                attrs = dict(row)
                return cls(**attrs)

            return None

        try:
            rows = connection.cursor().execute(request).fetchall()
        except OperationalError as e:
            print('Unable to get: ' + str(e))
            return None

        if rows:
            queryset = []
            for row in rows:
                attrs = dict(row)
                queryset.append(cls(**attrs))

            return queryset

        return None

    @classmethod
    def all(cls, **kwargs):
        kwargs.update(request_type='all')
        return cls.__db_getter(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        kwargs.update(request_type='one')
        return cls.__db_getter(**kwargs)

    @classmethod
    def filter(cls, **kwargs):
        kwargs.update(request_type='filter')
        return cls.__db_getter(**kwargs)

    def update(self, **kwargs):

        params = ', '.join(
            ['='.join((str(k), repr(v) if isinstance(v, str) else str(v))) for k, v in kwargs.items()]
        )

        connection = connect_to_db()

        request = f'UPDATE {self.__class__.__get_table_name()} SET {params} WHERE id={self.id};'
        print_raw_request(request)

        try:
            connection.cursor().execute(request)
            connection.commit()
        except OperationalError as e:
            print('Unable to update table: ' + str(e))
