import os
import configparser

custom_config_ini = os.path.join(os.getcwd(), 'config.ini')


config = configparser.ConfigParser()
config.read(custom_config_ini)

try:
    db_name = config.get('DB_SETTINGS', 'db_name')
except configparser.Error:
    db_name = 'default.db'

try:
    PATH_TO_DB = config.get('DB_SETTINGS', 'path_to_db')
    FULL_PATH_TO_DB = os.path.join(PATH_TO_DB, db_name)
except configparser.Error:
    PATH_TO_DB = os.getcwd()
    FULL_PATH_TO_DB = os.path.join(PATH_TO_DB, db_name)

try:
    FOREIGN_KEYS_CONTROL = config.getboolean('DB_SETTINGS', 'control_foreign_keys')
except configparser.Error:
    FOREIGN_KEYS_CONTROL = False

try:
    PRINT_REQUESTS = config.getboolean('DB_SETTINGS', 'print_sql_requests')
except configparser.Error:
    PRINT_REQUESTS = True



