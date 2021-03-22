'''
Структура файла конфигурации:
* token - ключ для бота, генерирует BotFather
* db_file - путь до файла БД
'''

import configparser

# Получение токена бота из конфига
def get_token():
    config = configparser.ConfigParser()
    config.read('data\config.cfg')
    token = config.get('main', 'token')
    return token

# Получение название файла с БД из конфига
def get_DB():
    config = configparser.ConfigParser()
    config.read('data\config.cfg')
    db_file = config.get('main', 'db_file')
    return db_file