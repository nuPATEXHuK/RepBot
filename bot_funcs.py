from sqlighter import SQLighter
import config_loader as cl

db = SQLighter(cl.get_DB())

def get_user_title(user_id, chat_id):
    title_from_db = str_from_db_answer(SQLighter.get_user_title(db, user_id, chat_id)[0]).strip()
    if (title_from_db == "None"):
        return "сударь"
    else:
        return title_from_db

def check_and_get_username(username):
    if (username[0] == '@'):
        return username[1:]
    else:
        return username

def set_user_title(from_user, chat_id, parameters):
    admin = int_from_db_answer(SQLighter.check_is_admin(db, from_user, chat_id)[0])
    if (admin == 0):
        user_title = get_user_title(from_user, chat_id)
        return "Вы, {} {}, не вправе давать титул.".format(user_title, str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0]))
    username = check_and_get_username(parameters[0])
    user_id = int_from_db_answer(SQLighter.get_id_by_username(db, username)[0])
    # TODO: проверить правильность титула (отсутсвие спецсимволов)
    title = parameters[1]
    if (user_id == 0 or SQLighter.check_chat_id(db, user_id, chat_id) == []):
        return "Сожалею, но я не знаю сударя {}. Возможно, вы имели в виду кого-то другого?".format(username)
    else:
        SQLighter.set_user_title(db, title, user_id, chat_id)
        return "Правом, данным мне свыше моим разработчиком, нарекаю сударя {} званием {}! Прими мои поздравления!".format(username, title)

# Функция для преобразования ответа от БД в число.
def int_from_db_answer(db_answer):
    answer = str(db_answer).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
    if (answer == ""):
        return 0
    else:
        return int(answer)

# Функция для преобразования ответа от БД в строку.
def str_from_db_answer(db_answer):
    return str(db_answer).replace("(", "").replace(")", "").replace(",", "").replace("'", "")

# Проверка строки на повышение или понижение репутации.
def change_rep(chat_id, message, from_user, to_user):
    answer = ""
    if (from_user != to_user):
        from_username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
        from_username_title = get_user_title(from_user, chat_id)
        to_username = str_from_db_answer(SQLighter.get_username_by_id(db, to_user)[0])
        to_username_title = get_user_title(to_user, chat_id)
        if (message == "+"):
            current_rep = int_from_db_answer(SQLighter.get_rep(db, to_user, chat_id)[0])
            free_rep = int_from_db_answer(SQLighter.get_free_rep(db, from_user, chat_id)[0])
            if (free_rep > 0):
                SQLighter.change_rep(db, to_user, chat_id, current_rep + 1)
                SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 1)
                answer = str.format("{} {} испытывает глубое уважение к {} {}.\nПочтение к последнему растёт и составляет уже {}.", from_username_title.title(), from_username, to_username_title, to_username, current_rep + 1)
            else:
                answer = str.format("{} {} испытывает глубое уважение к {} {}.\nНо бал него уже окончен, своё почтение он сможет выразить только завтра.", from_username_title.title(), from_username, to_username_title, to_username)
        if (message == "-"):
            current_rep = int_from_db_answer(SQLighter.get_rep(db, to_user, chat_id)[0])
            free_rep = int_from_db_answer(SQLighter.get_free_rep(db, from_user, chat_id)[0])
            if (free_rep > 0):
                SQLighter.change_rep(db, to_user, chat_id, current_rep - 1)
                SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 1)
                answer = str.format("{} {} выражает своё разочарование {} {}.\nРепутация подмочена и составляет {}.", from_username_title.title(), from_username, to_username_title, to_username, current_rep - 1)
            else:
                answer = str.format("{} {} выражает своё разочарование {} {}.\nПравда, в своём имении его уже никто не слышит, так что он может выразить свои чувства завтра.", from_username_title.title(), from_username, to_username_title, to_username)
    else:
        if (message == "+"):
            username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
            answer = str.format("Ничего-ничего, голубчик {}, нарциссизм лечится.", username)
            current_rep = int_from_db_answer(SQLighter.get_rep(db, from_user, chat_id)[0])
        if (message == "-"):
            username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
            username_title = get_user_title(from_user, chat_id)
            answer = str.format("А {} {} знает толк в извращениях...", username_title, username)
            current_rep = int_from_db_answer(SQLighter.get_rep(db, from_user, chat_id)[0])
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
    current_messages_count = int_from_db_answer(SQLighter.get_message_count_stat(db, from_user, chat_id)[0])
    current_char_count = int_from_db_answer(SQLighter.get_char_count_stat(db, from_user, chat_id)[0])
    
    SQLighter.add_message_stat(db, current_messages_count + 1, current_char_count + char_count, chat_id, from_user)

def get_all_activity(chat_id):
    user_activity = SQLighter.get_all_activity(db, chat_id)
    activity = 0
    for user_activity_from_bd in user_activity:
        activity += user_activity_from_bd[0]
    return activity

def get_user_activity(user_id, chat_id):
    user_activity = int_from_db_answer(SQLighter.get_user_activity(db, user_id, chat_id)[0])
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
    title = "Титул: {}".format(get_user_title(user_id, chat_id).title())
    result_text += title + CR
    activity = "Активность: {}%".format(get_user_activity(user_id, chat_id))
    result_text += activity + CR
    messages = "Сообщений: {}".format(int_from_db_answer(SQLighter.get_message_count_stat(db, user_id, chat_id)[0]))
    result_text += messages + CR
    top = "Место в топе: {}".format("[в разработке]")
    result_text += top + CR
    rep = "Репутация: {}".format(int_from_db_answer(SQLighter.get_rep(db, user_id, chat_id)[0]))
    result_text += rep + CR
    free_rep = "Свободных очков репутации: {}".format(int_from_db_answer(SQLighter.get_free_rep(db, user_id, chat_id)[0]))
    result_text += free_rep + CR
    
    status = result_text + line
    return status