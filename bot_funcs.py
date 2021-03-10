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
    if (username == ""):
        return ""
    if (username[0] == '@'):
        return username[1:]
    else:
        return username

def check_is_admin(user_id, chat_id):
    admin = int_from_db_answer(SQLighter.check_is_admin(db, user_id, chat_id)[0])
    if (admin == 0):
        user_title = get_user_title(user_id, chat_id)
        return "{} {}, у вас недостаточно прав для выполнения этой команды.".format(user_title, str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]))
    else:
        return ""

def set_user_title(from_user, chat_id, parameters):
    check_admin = check_is_admin(from_user, chat_id)
    if (check_admin != ""):
        return check_admin
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
            current_rep_pos_offset = int_from_db_answer(SQLighter.get_rep_pos_offset(db, to_user, chat_id)[0])
            free_rep = int_from_db_answer(SQLighter.get_free_rep(db, from_user, chat_id)[0])
            if (free_rep > 0):
                SQLighter.change_rep(db, to_user, chat_id, current_rep + 1)
                SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 1)
                SQLighter.change_pos_rep(db, to_user, chat_id, current_rep_pos_offset + 1)
                answer = str.format("{} {} испытывает глубокое уважение к {} {}.\nПочтение к последнему растёт и составляет уже {}.", from_username_title.title(), from_username, to_username_title, to_username, current_rep + 1)
            else:
                answer = str.format("{} {} испытывает глубокое уважение к {} {}.\nНо бал для него уже окончен, своё почтение он сможет выразить только завтра.", from_username_title.title(), from_username, to_username_title, to_username)
        if (message == "-"):
            current_rep = int_from_db_answer(SQLighter.get_rep(db, to_user, chat_id)[0])
            current_rep_neg_offset = int_from_db_answer(SQLighter.get_rep_neg_offset(db, to_user, chat_id)[0])
            free_rep = int_from_db_answer(SQLighter.get_free_rep(db, from_user, chat_id)[0])
            if (free_rep > 0):
                SQLighter.change_rep(db, to_user, chat_id, current_rep - 1)
                SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 1)
                SQLighter.change_neg_rep(db, to_user, chat_id, current_rep_neg_offset + 1)
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

def restore_standard_rep():
    user_list = SQLighter.get_users_list(db)
    for user_id_from_bd in user_list:
        user_id = str_from_db_answer(user_id_from_bd)
        SQLighter.restore_free_rep(db, user_id, 10)
        SQLighter.restore_neg_and_pos_rep(db, user_id)

def restore_free_rep_for_user(from_user, to_user, chat_id, free_rep):
    check_admin = check_is_admin(from_user, chat_id)
    if (check_admin != ""):
        return check_admin
    try:
        free_rep = int(free_rep)
    except:
        free_rep = 0
    if (free_rep < 1):
        free_rep = 0
    to_user_id = int_from_db_answer(SQLighter.get_id_by_username(db, check_and_get_username(to_user))[0])
    current_free_rep = int_from_db_answer(SQLighter.get_free_rep(db, to_user_id, chat_id)[0])
    from_username_title = get_user_title(from_user, chat_id).title()
    from_username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
    to_username_title = get_user_title(to_user_id, chat_id)
    to_username = str_from_db_answer(SQLighter.get_username_by_id(db, to_user_id)[0])
    if (free_rep > 0):
        SQLighter.restore_free_rep_for_user(db, to_user_id, chat_id, current_free_rep + free_rep)
        return "{} {} великодушно восстановил доступные очки репутации для {} {}.\nТеперь их стало {}.".format(from_username_title, from_username, to_username_title, to_username, current_free_rep + free_rep)
    else:
        return "{} {} попытался восстановить доступные очки репутации у {} {}, но что-то пошло не так.".format(from_username_title, from_username, to_username_title, to_username)

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

def get_my_top(user_id, username, chat_id):
    user_title = get_user_title(user_id, chat_id)
    answer = "Топ {} {}:\n\n".format(user_title, username)
    answer += get_user_top_message(user_id, chat_id, True)
    answer += get_user_top_rep(user_id, chat_id, True)
    return answer

def get_top_message(user_id, chat_id, count):
    check_admin = check_is_admin(user_id, chat_id)
    if (check_admin != ""):
        return check_admin
    try:
        count = int(count)
    except:
        may_be_user = check_and_get_username(count)
        count = 0
    if (count < 1):
        count = 0
    try:
        to_user = int_from_db_answer(SQLighter.get_id_by_username(db, may_be_user)[0])
    except:
        to_user = ""
    if (to_user == ""):
        count_msg = ""
        if (count > 0):
            count_msg = "-{}".format(count)
        top_msg_list = SQLighter.get_top_message_list(db, chat_id, count)
        answer = "Топ{} по количеству сообщений:\n".format(count_msg)
        i = 1
        for top_user in top_msg_list:
            user_and_msg = str_from_db_answer(top_user).split(" ")
            user_id = user_and_msg[0]
            username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
            msg_count = user_and_msg[1]
            answer += "{}. {} {}. Сообщений: {}\n".format(i, get_user_title(user_id, chat_id).title(), username, msg_count)
            i += 1
        return answer
    else:
        return get_user_top_message(to_user, chat_id, False)

def get_top_rep(user_id, chat_id, count):
    check_admin = check_is_admin(user_id, chat_id)
    if (check_admin != ""):
        return check_admin
    try:
        count = int(count)
    except:
        may_be_user = check_and_get_username(count)
        count = 0
    if (count < 1):
        count = 0
    try:
        to_user = int_from_db_answer(SQLighter.get_id_by_username(db, may_be_user)[0])
    except:
        to_user = ""
    if (to_user == ""):
        count_rep = ""
        if (count > 0):
            count_rep = "-{}".format(count)
        top_rep_list = SQLighter.get_top_rep_list(db, chat_id, count)
        answer = "Топ{} по репутации:\n".format(count_rep)
        i = 1
        for top_user in top_rep_list:
            user_and_rep = str_from_db_answer(top_user).split(" ")
            user_id = user_and_rep[0]
            username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
            rep_count = user_and_rep[1]
            answer += "{}. {} {}. Репутация: {}\n".format(i, get_user_title(user_id, chat_id).title(), username, rep_count)
            i += 1
        return answer
    else:
        return get_user_top_rep(to_user, chat_id, False)

def get_user_top_message(user_id, chat_id, my_stat):
    top_msg_list = SQLighter.get_top_message_list(db, chat_id, 0)
    user_msg = int_from_db_answer(SQLighter.get_message_count_stat(db, user_id, chat_id)[0])
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    i = 1
    answer = "{}, тебя нет в топе. Обратись к администратору бота.".format(username)
    if (my_stat):
        for top_user in top_msg_list:
            user_and_msg = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_msg[0])):
                answer = "Сообщений: {}\nРанг в топе по сообщениям: {}\n".format(user_msg, i)
            i += 1
    else:
        for top_user in top_msg_list:
            user_and_msg = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_msg[0])):
                answer = "{} {}.\nСообщений: {}\nРанг в топе: {}\n".format(get_user_title(user_id, chat_id).title(), username, user_msg, i)
            i += 1
    return answer

def get_user_top_rep(user_id, chat_id, my_stat):
    top_rep_list = SQLighter.get_top_rep_list(db, chat_id, 0)
    user_rep = int_from_db_answer(SQLighter.get_rep(db, user_id, chat_id)[0])
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    i = 1
    answer = "{}, тебя нет в топе. Обратись к администратору бота.".format(username)
    if (my_stat):
        for top_user in top_rep_list:
            user_and_rep = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_rep[0])):
                answer = "Репутация: {}\nРанг в топе по репутации: {}\n".format(user_rep, i)
            i += 1
    else:
        for top_user in top_rep_list:
            user_and_rep = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_rep[0])):
                answer = "{} {}.\nРепутация: {}\nРанг в топе: {}\n".format(get_user_title(user_id, chat_id).title(), username, user_rep, i)
            i += 1
    return answer

def get_main_pos(chat_id):
    top_user_id = int_from_db_answer(SQLighter.get_user_id_by_top_rep_pos_offset(db, chat_id)[0])
    top_user_rep_offset = int_from_db_answer(SQLighter.get_rep_pos_offset(db, top_user_id, chat_id)[0])
    if (top_user_rep_offset > 0):
        top_username = str_from_db_answer(SQLighter.get_username_by_id(db, top_user_id)[0])
        top_user_title = str_from_db_answer(SQLighter.get_user_title(db, top_user_id, chat_id)[0])
        return "Главный красавчик чата на сегодня - {} {}.\nСобрано плюсов: {}".format(top_user_title, top_username, top_user_rep_offset)
    else:
        return "Ну и ну, на сегодня пока не видно красавчиков в этом чате.\nЧто, никто не заслужил похвалы?"

def get_main_neg(chat_id):
    top_user_id = int_from_db_answer(SQLighter.get_user_id_by_top_rep_neg_offset(db, chat_id)[0])
    top_user_rep_offset = int_from_db_answer(SQLighter.get_rep_neg_offset(db, top_user_id, chat_id)[0])
    if (top_user_rep_offset > 0):
        top_username = str_from_db_answer(SQLighter.get_username_by_id(db, top_user_id)[0])
        top_user_title = str_from_db_answer(SQLighter.get_user_title(db, top_user_id, chat_id)[0])
        return "Сегодня все дружно булили {} {}.\nСобрано минусов: {}".format(top_user_title, top_username, top_user_rep_offset)
    else:
        return "Ох, какие же сегодня все лапоньки в чате. :З\nДружба, жвачка и никаких минусов?"

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
    messages = get_user_top_message(user_id, chat_id, True)
    result_text += messages
    rep = get_user_top_rep(user_id, chat_id, True)
    result_text += rep
    free_rep = "Свободных очков репутации: {}".format(int_from_db_answer(SQLighter.get_free_rep(db, user_id, chat_id)[0]))
    result_text += free_rep + CR
    
    status = result_text + line
    return status

def get_help(user_id, chat_id):
    admin = True
    check_admin = check_is_admin(user_id, chat_id)
    if (check_admin != ""):
        admin = False
    command_list = "Список доступных команд:\n"
    command_list += "● /top_my - вызов своей статистики только по топам\n"
    command_list += "● /stat - вызов своей общей статистики\n"
    command_list += "● \"+\" или \"-\" в ответ на сообщение другого пользователя - изменение репутации пользователя"
    command_list += "● /main_pos - кто сегодня собрал больше всех плюсов?"
    command_list += "● /main_neg - кто сегодня собрал больше всех минусов?"
    if (admin):
        command_list += "\n● /add_free_rep [username] [count] - добавить свободные очки репутации (count) пользователю (username)\n"
        command_list += "● /top_message [username / count] - вызов топа по сообщениям у конкретного пользователя (username) или по количеству (count)\n"
        command_list += "● /top_rep [username / count] - вызов топа по репутации у конкретного пользователя (username) или по количеству (count)\n"
        command_list += "● /assign_title [username] [title] - добавить титул (title) пользователю (username)"
    return command_list
