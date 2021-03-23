'''
Структура файла конфигурации:
* token - ключ для бота, генерирует BotFather
* db_file - путь до файла БД
'''

import configparser
import os

if (os.name == 'nt'):
    config_path = 'data\\config_windows.cfg'
else:
    config_path = 'data/config_linux.cfg'

# Получение токена бота из конфига
def get_token():
    config = configparser.ConfigParser()
    config.read(config_path)
    token = config.get('main', 'token')
    return token

# Получение название файла с БД из конфига
def get_DB():
    config = configparser.ConfigParser()
    config.read(config_path)
    db_file = config.get('main', 'db_file')
    return db_file