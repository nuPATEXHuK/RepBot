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

# Функция для преобразования ответа от БД в число.
def int_from_db_answer(db_answer):
    return int(db_answer.replace("(", "").replace(")", "").replace(",", "").replace("'", ""))

# Функция для преобразования ответа от БД в строку.
def str_from_db_answer(db_answer):
    return str(db_answer).replace("(", "").replace(")", "").replace(",", "").replace("'", "")

# Проверка строки на повышение или понижение репутации.
def change_rep(chat_id, message, from_user, to_user):
    answer = ""
    if (from_user != to_user):
        from_username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
        to_username = str_from_db_answer(SQLighter.get_username_by_id(db, to_user)[0])
        if (message == "+"):
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, to_user, chat_id)[0]))
            free_rep = int_from_db_answer(str(SQLighter.get_free_rep(db, from_user, chat_id)[0]))
            if (free_rep > 0):
                SQLighter.change_rep(db, to_user, chat_id, current_rep + 1)
                SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 1)
                answer = str.format("Сударь {} испытывает глубое уважение к сударю {}.\nПочтение к последнему растёт и составляет уже {}.", from_username, to_username, current_rep + 1)
            else:
                answer = str.format("Сударь {} испытывает глубое уважение к сударю {}.\nНо бал него уже окончен, своё почтение он сможет выразить только завтра.", from_username, to_username)
        if (message == "-"):
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, to_user, chat_id)[0]))
            free_rep = int_from_db_answer(str(SQLighter.get_free_rep(db, from_user, chat_id)[0]))
            if (free_rep > 0):
                SQLighter.change_rep(db, to_user, chat_id, current_rep - 1)
                SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 1)
                answer = str.format("Сударь {} выражает разочарование сударем {}.\nРепутация подмочена и составляет {}.", from_username, to_username, current_rep - 1)
            else:
                answer = str.format("Сударь {} выражает разочарование сударем {}.\nПравда, в своём имении его уже никто не слышит, так что он может выразить свои чувства завтра.", from_username, to_username)
    else:
        if (message == "+"):
            username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
            answer = str.format("Ничего-ничего, голубчик {}, нарциссизм лечится.", username)
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, from_user, chat_id)[0]))
        if (message == "-"):
            username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
            answer = str.format("А сударь {} знает толк в извращениях...", username)
            current_rep = int_from_db_answer(str(SQLighter.get_rep(db, from_user, chat_id)[0]))
    return answer

def get_all_conferences():
    return ""

def restore_free_rep():
    user_list = SQLighter.get_users_list(db)
    for user_id_from_bd in user_list:
        user_id = str_from_db_answer(user_id_from_bd)
        SQLighter.restore_free_rep(db, user_id)

# Обновление статистики (добавление сообщений/активности).
def add_message_stat(chat_id, from_user, username, char_count):
    if (SQLighter.get_username_by_id(db, from_user) == []):
        SQLighter.add_new_user(db, from_user, username)
        SQLighter.add_new_stat(db, from_user, chat_id)
    if (SQLighter.check_chat_id(db, from_user, chat_id) == []):
        SQLighter.add_new_stat(db, from_user, chat_id)
    current_messages_count = int_from_db_answer(str(SQLighter.get_message_count_stat(db, from_user, chat_id)[0]))
    current_char_count = int_from_db_answer(str(SQLighter.get_char_count_stat(db, from_user, chat_id)[0]))
    
    SQLighter.add_message_stat(db, current_messages_count + 1, current_char_count + char_count, chat_id, from_user)

def get_all_activity(chat_id):
    user_activity = SQLighter.get_all_activity(db, chat_id)
    activity = 0
    for user_activity_from_bd in user_activity:
        activity += user_activity_from_bd[0]
    return activity

def get_user_activity(user_id, chat_id):
    user_activity = int_from_db_answer(str(SQLighter.get_user_activity(db, user_id, chat_id)[0]))
    all_activity = get_all_activity(chat_id)
    if (all_activity != 0):
        return round(user_activity / all_activity * 100, 2)
    else:
        return "Активность чата отсуствует"

# Формирование статуса.
def status_by_user(user_id, chat_id):
    line = "_____________________"
    CR = "\n"
    result_text = line + CR
    name = "Имя: {}".format(str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]))
    result_text += name + CR
    activity = "Активность: {}%".format(get_user_activity(user_id, chat_id))
    result_text += activity + CR
    messages = "Сообщений: {}".format(int_from_db_answer(str(SQLighter.get_message_count_stat(db, user_id, chat_id)[0])))
    result_text += messages + CR
    top = "Место в топе: {}".format("[в разработке]")
    result_text += top + CR
    rep = "Репутация: {}".format(int_from_db_answer(str(SQLighter.get_rep(db, user_id, chat_id)[0])))
    result_text += rep + CR
    free_rep = "Свободных очков репутации: {}".format(int_from_db_answer(str(SQLighter.get_free_rep(db, user_id, chat_id)[0])))
    result_text += free_rep + CR
    
    status = result_text + line
    return status