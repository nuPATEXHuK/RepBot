import re

from sqlighter import SQLighter
import config_loader as cl

db = SQLighter(cl.get_DB())

# Функция для возврата ключа по значению.
# Пример: на входе список типа {Test1 : 12345, Test: 23456}, и нужный ID=12345, на выходе получаем имя "Test1".
def get_key_by_value(value_list, value):
    key = None
    for current_key, current_value in value_list.items():
        if current_value == value:
            key = current_key
    return key

def int_from_db_answer(db_answer):
    return int(db_answer.replace("(", "").replace(")", "").replace(",", ""))

def str_from_db_answer(db_answer):
    return str(db_answer).replace("(", "").replace(")", "").replace(",", "").replace("'", "")

# Проверка строки на повышение или понижение репутации
def change_rep(chat_id, message, from_user, to_user):
    answer = ""
    if (from_user != to_user):
        from_username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
        to_username = str_from_db_answer(SQLighter.get_username_by_id(db, to_user)[0])
        if (message == "+"):
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, to_user, chat_id)[0]))
            SQLighter.change_rep(db, to_user, chat_id, current_rep + 1)
            answer = str.format("@{} мур-мур-муркает на @{}. Кавай-ня! ☺️\nРепутация повышена!", from_username, to_username)
        if (message == "-"):
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, to_user, chat_id)[0]))
            SQLighter.change_rep(db, to_user, chat_id, current_rep - 1)
            answer = str.format("@{} обзывает \"бакой\" @{}. 😡\nРепутация снижена!", from_username, to_username)
    else:
        if (message == "+"):
            username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
            answer = str.format("@{}, пытаешься сжульничать? Баааака! Кусь тебя! 😈\nРепутация снижена!", username)
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, from_user, chat_id)[0]))
            SQLighter.change_rep(db, from_user, chat_id, current_rep - 1)
        if (message == "-"):
            username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
            answer = str.format("@{}, да ты, погляжу, М-тип? Мне нравится, продолжай. 😏\nРепутация снижена!", username)
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, from_user, chat_id)[0]))
            SQLighter.change_rep(db, from_user, chat_id, current_rep - 1)
    return answer

def get_all_conferences():
    return ""

def add_message_stat(chat_id, from_user, username, char_count):
    if (SQLighter.get_username_by_id(db, from_user) == []):
        SQLighter.add_new_user(db, from_user, username, chat_id)
    current_messages_count = int_from_db_answer(str(SQLighter.get_message_count_stat(db, from_user, chat_id)[0]))
    current_char_count = int_from_db_answer(str(SQLighter.get_char_count_stat(db, from_user, chat_id)[0]))
    
    SQLighter.add_message_stat(db, current_messages_count + 1, current_char_count + char_count, chat_id, from_user)

# Формирование справки.
def status_by_user(user_id, chat_id):
    line = "_____________________"
    name = "Имя: {}".format(str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]))
    activity = "Активность: {}".format("[в разработке]")
    messages = "Сообщений: {}".format(int_from_db_answer(str(SQLighter.get_message_count_stat(db, user_id, chat_id)[0])))
    top = "Место в топе: {}".format("[в разработке]")
    rep = "Репутация: {}".format(int_from_db_answer(str(SQLighter.get_rep(db, user_id, chat_id)[0])))
    CR = "\n"

    status = str.format("{line}{cr}{name}{cr}{activity}{cr}{messages}{cr}{top}{cr}{rep}{cr}{line}", line=line, cr=CR, name=name, activity=activity, messages=messages, top=top, rep=rep)
    return status