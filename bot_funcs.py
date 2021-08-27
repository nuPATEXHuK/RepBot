from sqlighter import SQLighter
import config_loader as cl
import dialogs
from operator import itemgetter

db = SQLighter(cl.get_DB())

random_events = ["nothing", "add_free_rep", "lose_free_rep", "add_rep", "lose_rep", "add_gold", "lose_gold"]
buildings = ["temple", "casino", "fair"]
buildings_list = {
    "temple": "храма", 
    "casino": "казино", 
    "fair": "ярмарки"
}
shop_items = {
    "admin1": 150,
    "admin3": 400,
    "admin7": 900,
    "title_pidor1": 100,
    "title_pidor2": 300,
    "title_pidor3": 1000,
    "title_thief1": 100,
    "title_thief2": 300,
    "title_thief3": 500,
    "title_bandit1": 100,
    "title_bandit2": 300,
    "title_bandit3": 800,
    "title_robber1": 100,
    "title_robber2": 500,
    "title_robber3": 1000,
    "title_soldier1": 100,
    "title_soldier2": 500,
    "title_soldier3": 1000,
    "title_soldier4": 3000,
    "title_wolf": 100,
    "title_pirate": 1000,
    "title_legend": 9000,
    "free_rep1": 50,
    "free_rep5": 200,
    "free_rep10": 400,
    "fight_dice": 200,
    "fight_add_dice": 400,
    "fight_immune1": 200,
    "fight_immune3": 500,
    "fight_immune7": 1000,
    "fight_resurrection": 100
}
titles = {
    "title_pidor1": "латентный пидор",
    "title_pidor2": "пидор дня",
    "title_pidor3": "легендарный пидор",
    "title_thief1": "мелкий воришка",
    "title_thief2": "почётный вор",
    "title_thief3": "главарь воров",
    "title_bandit1": "бандит",
    "title_bandit2": "бывалый бандит",
    "title_bandit3": "главарь бандитов",
    "title_robber1": "грабитель",
    "title_robber2": "опытный грабитель",
    "title_robber3": "неуловимый грабитель",
    "title_soldier1": "рядовой",
    "title_soldier2": "сержант",
    "title_soldier3": "полковник",
    "title_soldier4": "генерал",
    "title_wolf": "волк-одиночка",
    "title_pirate": "информатор",
    "title_legend": "легенда"
}
revolvers = {}
chat_games = {}
last_winner = {}
active_roulette = False

def get_user_title(user_id, chat_id):
    title_from_db = str_from_db_answer(SQLighter.get_user_title(db, user_id, chat_id)[0]).strip()
    if (title_from_db == "None" or title_from_db == ""):
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
        user_title = get_user_title(user_id, chat_id).title()
        return "{} {}, у вас недостаточно прав для выполнения этой команды.".format(user_title, str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]))
    else:
        return ""

# Грабительство караванов
def rob_caravan(user_id, chat_id):
    if today_caravan_available(user_id, chat_id):
        gold = dialogs.get_random_int(-100, 100)
        current_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
        if gold < 1:
            if current_gold > -gold:
                answer = f"Грабёж каравана прошёл неудачно. Ты потерял {-gold} золота. У тебя осталось {current_gold + gold} золота."
                SQLighter.set_gold(db, user_id, chat_id, current_gold + gold)
            else:
                answer = f"Грабёж каравана прошёл неудачно. Ты потерял все деньги и остался с пустыми карманами."
                SQLighter.set_gold(db, user_id, chat_id, 0)
        else:
            SQLighter.set_gold(db, user_id, chat_id, current_gold + gold)
            answer = f"Грабёж каравана прошёл успешно. Ты награбил {gold} золотых. Сейчас у тебя {current_gold + gold} золотых."
        current_today_caravan_available = int_from_db_answer(SQLighter.get_today_caravan_available(db, user_id, chat_id)[0])
        SQLighter.set_today_caravan_available(db, user_id, chat_id, current_today_caravan_available - 1)
    else:
        answer = "На сегодня попытки грабительства израсходованы. Возвращайтесь завтра."
    return answer

# Грабительство игроков
def rob_player(from_user_id, to_user_id, chat_id):
    if not today_caravan_available(from_user_id, chat_id):
        return "На сегодня попытки грабительства израсходованы. Возвращайтесь завтра."
    to_username = str_from_db_answer(SQLighter.get_username_by_id(db, to_user_id)[0])
    from_username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user_id)[0])
    from_username_title = get_user_title(from_user_id, chat_id).capitalize()
    to_username_title = get_user_title(to_user_id, chat_id)
    answer = f"{from_username_title} {from_username} пытается ограбить {to_username_title} {to_username}.\n"
    if (from_user_id != to_user_id):
        i = dialogs.get_random_int(1, 6)
        dice_mod = str_from_db_answer(SQLighter.get_dice_mod(db, from_user_id, chat_id)[0])
        add_sum_dice = int(dice_mod[1])
        add_dice = int(dice_mod[3])
        if add_sum_dice > 0:
            i += add_sum_dice
            answer += f"{from_username_title} {from_username} умело использует подкрутку и увеличивает результат своего броска кубика на {add_sum_dice}.\n"
        if add_dice > 0:
            while add_dice > 0:
                j = dialogs.get_random_int(1, 6)
                i += j
                answer += f"{from_username_title} {from_username} обходит правила и кидает ещё один кубик. Выпадает {j}.\n"
                add_dice -= 1
        caravan_available = int_from_db_answer(SQLighter.get_today_caravan_available(db, from_user_id, chat_id)[0])
        SQLighter.set_today_caravan_available(db, from_user_id, chat_id, caravan_available - 1)
        current_immune_days = int_from_db_answer(SQLighter.get_immune_days(db, to_user_id, chat_id)[0])
        if current_immune_days > 0:
            answer += f"{from_username_title} {from_username} атакует {to_username_title} {to_username}, но в дело вмешиваются мистические силы. Атака провалилась, золото осталось у его владельца."
            return answer
        current_gold_to_user = int_from_db_answer(SQLighter.get_gold(db, to_user_id, chat_id)[0])
        if current_gold_to_user > 0:
            steal_gold = dialogs.get_random_int(1, current_gold_to_user)
        else:
            answer += f"{to_username_title.capitalize()} {to_username} выворачивает карманы, а там нет ни единого золотого."
            return answer
        if (i < 4):
            answer += f"\nРезультат броска: {i} из 6. Неудача!\n\nОграбление прошло неудачно и {from_username_title} {from_username} уходит ни с чем."
        else:
            current_gold_from_user = int_from_db_answer(SQLighter.get_gold(db, from_user_id, chat_id)[0])
            if (i < 6):
                SQLighter.set_gold(db, from_user_id, chat_id, current_gold_from_user + steal_gold)
                SQLighter.set_gold(db, to_user_id, chat_id, current_gold_to_user - steal_gold)
                answer += f"\nРезультат броска: {i} из 6.\n\n{from_username_title} {from_username} устраивает засаду и успешно грабит {to_username_title} {to_username}, пока тот в панике защищается.\nКоличество похищенного золота: {steal_gold}."
            else:
                steal_gold = current_gold_to_user
                SQLighter.set_gold(db, from_user_id, chat_id, current_gold_from_user + steal_gold)
                SQLighter.set_gold(db, to_user_id, chat_id, 0)
                answer += f"\nРезультат броска: {i} из 6.\n\n{from_username_title} {from_username} проводит настолько идеальную воровскую операцию, что {to_username_title} {to_username} даже не замечает, как всё его золото куда-то исчезло.\nКоличество похищенного золота: {steal_gold}"
    else:
        answer = f"{from_username_title} {from_username} пытается ограбить сам себя. Эм... с тобой всё хорошо?"
    return answer

def today_caravan_available(user_id, chat_id):
    return int_from_db_answer(SQLighter.get_today_caravan_available(db, user_id, chat_id)[0]) > 0

def get_shop(group):
    if group is None or group == "":
        shop_list = "Добро пожаловать в магазин бота. Товаров сейчас много, поэтому введите одну из интересующих вас категорий через пробел после команды /shop:\n"
        shop_list += "● Админка в чате: admin\n"
        shop_list += "● Титулы: title\n"
        shop_list += "● Очки действий: free\n"
        shop_list += "● Бои и рулетка: fight\n"
        return shop_list
    
    shop_list = "Вот что сейчас есть в наличии:\n"
    if group == "admin":
        shop_list += "\n=== Админка в чате ===\n"
        shop_list += "● Админка в чате на 1 день - 150 золотых.\nКод для покупки: admin1\n"
        shop_list += "● Админка в чате на 3 дня - 400 золотых.\nКод для покупки: admin3\n"
        shop_list += "● Админка в чате на 7 дней - 900 золотых.\nКод для покупки: admin7\n"
        return shop_list
    if group == "title":
        shop_list += "\n=== Титулы ===\n"
        for title_code in titles.keys():
            shop_list += f"● Титул \"{titles[title_code].capitalize()}\" - {shop_items[title_code]} золотых.\nКод для покупки: {title_code}\n"
        return shop_list
    if group == "free":
        shop_list += "\n=== Очки действий ===\n"
        shop_list += "● 1 свободное очко действий - 50 золотых.\nКод для покупки: free_rep1\n"
        shop_list += "● 5 свободных очков действий - 200 золотых.\nКод для покупки: free_rep5\n"
        shop_list += "● 10 свободных очков действий - 400 золотых.\nКод для покупки: free_rep10\n"
        return shop_list
    if group == "fight":
        shop_list += "\n=== Бои и рулетка ===\n"
        shop_list += "● Подкрутка кубика на +1 (на день) - 200 золотых. \nКод для покупки: fight_dice\n"
        shop_list += "● Бросок дополнительного кубика (на день) - 400 золотых. \nКод для покупки: fight_add_dice\n"
        shop_list += "● Иммунитет к атакам на 1 день - 200 золотых. \nКод для покупки: fight_immune1\n"
        shop_list += "● Иммунитет к атакам на 3 дня - 500 золотых. \nКод для покупки: fight_immune3\n"
        shop_list += "● Иммунитет к атакам на 7 дней - 1000 золотых. \nКод для покупки: fight_immune7\n"
        shop_list += "● Воскрешение в рулетке - 100 золотых. \nКод для покупки: fight_resurrection\n"
        return shop_list
    return "Вы указали несуществующую категорию товаров."

def buy(user_id, chat_id, item):
    if item not in shop_items.keys():
        return "Такого предмета нет в магазине. Укажите правильный предмет."
    price = shop_items[item]
    hand_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
    bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, user_id, chat_id)[0])
    user_gold = hand_gold + bank_gold
    if price > user_gold:
        return "Не хватает золота для покупки."
    else:
        if price > hand_gold:
            SQLighter.set_gold(db, user_id, chat_id, 0)
            SQLighter.set_bank_gold(db, user_id, chat_id, user_gold - price)
        else:
            SQLighter.set_gold(db, user_id, chat_id, hand_gold - price)
        if "admin" in item:
            add_days = int(item.replace("admin", ""))
            current_days = int_from_db_answer(SQLighter.get_admin_days(db, user_id, chat_id)[0])
            SQLighter.set_admin_days(db, user_id, chat_id, current_days + add_days)
            SQLighter.set_admin(db, user_id, chat_id, 1)
            return f"Покупка совершена успешно!\nОсталось дней с админкой: {current_days + add_days}."
        if "title" in item:
            title = titles[item]
            SQLighter.set_user_title(db, title, user_id, chat_id)
            return f"Покупка совершена успешно!\nТвой новый титул: {title}"
        if "free_rep" in item:
            add_free_rep = int(item.replace("free_rep", ""))
            current_free_rep = int_from_db_answer(SQLighter.get_free_rep(db, user_id, chat_id)[0])
            SQLighter.restore_free_rep(db, user_id, current_free_rep + add_free_rep)
            return f"Покупка совершена успешно!\nДобавлены свободные очки действий.\nОчков свободных действий сейчас: {current_free_rep + add_free_rep}."
        if "fight" in item:
            goods = item.replace("fight_", "")
            if goods == "dice":
                old_dice_mod = str_from_db_answer(SQLighter.get_dice_mod(db, user_id, chat_id)[0])
                new_add_dice = int(old_dice_mod[1]) + 1
                new_dice_mod = f"a{new_add_dice}d{old_dice_mod[3]}"
                SQLighter.set_dice_mod(db, user_id, chat_id, new_dice_mod)
                return f"Покупка совершена успешно!\nВ течение дня ваш результат броска кубика увеличивается на {new_add_dice} при атаке другого игрока."
            if goods == "add_dice":
                old_dice_mod = str_from_db_answer(SQLighter.get_dice_mod(db, user_id, chat_id)[0])
                new_add_dice = int(old_dice_mod[3]) + 1
                new_dice_mod = f"a{old_dice_mod[1]}d{new_add_dice}"
                SQLighter.set_dice_mod(db, user_id, chat_id, new_dice_mod)
                return f"Покупка совершена успешно!\nВ течение дня вы кидаете на {new_add_dice} больше кубиков при атаке другого игрока."
            if "immune" in goods:
                add_immune_days = int(goods.replace("immune", ""))
                current_immune_days = int_from_db_answer(SQLighter.get_immune_days(db, user_id, chat_id)[0])
                SQLighter.set_immune_days(db, user_id, chat_id, current_immune_days + add_immune_days)
                return f"Покупка совершена успешно!\nТеперь у вас есть защита от нападений игроков. Осталось дней с защитой: {current_immune_days + add_immune_days}"
            if "resurrection":
                SQLighter.restore_roulette_today(db, user_id)
                SQLighter.restore_free_roulette(db, user_id)
                return "Покупка совершена успешно!\nВы восрешены и можете снова играть в рулетку."

def send_money(from_user_id, chat_id, parameters):
    current_gold = int_from_db_answer(SQLighter.get_gold(db, from_user_id, chat_id)[0])
    current_bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, from_user_id, chat_id)[0])
    from_user_gold = current_gold + current_bank_gold
    to_username = check_and_get_username(parameters[0])
    to_user_id = int_from_db_answer(SQLighter.get_id_by_username(db, to_username)[0])
    to_user_gold = int_from_db_answer(SQLighter.get_bank_gold(db, to_user_id, chat_id)[0])
    try:
        send_gold = int(parameters[1])
    except:
        return "Указано неверное количество золота."
    if send_gold < 10 or from_user_gold < send_gold:
        return "Указано неверное количество золота или его у вас недостаточно для отправки. Минимальная суммая перевода - 5 золотых."
    else:
        commission = round(send_gold / 10)
        if commission > 100:
            commission = 100
        if send_gold > current_gold:
            send_gold -= current_gold
            SQLighter.set_gold(db, from_user_id, chat_id, 0)
            SQLighter.set_bank_gold(db, from_user_id, chat_id, current_bank_gold - send_gold)
            SQLighter.set_bank_gold(db, to_user_id, chat_id, to_user_gold + send_gold - commission)
        else:
            SQLighter.set_gold(db, from_user_id, chat_id, current_gold - send_gold)
            SQLighter.set_bank_gold(db, to_user_id, chat_id, to_user_gold + send_gold - commission)
        return f"Золото успешно переведено на счёт в банке другого игрока.\nКомиссия за перевод: {commission}."

def transfer_to_bank(user_id, chat_id, money):
    try:
        money = int(money)
    except:
        return "Указано неверное количество золота."
    if money < 1:
        return "Указано неверное количество золота или его у вас недостаточно для отправки в банк."
    current_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
    current_bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, user_id, chat_id)[0])
    if current_gold < 1 or money < 1 or money > current_gold:
        return "Недостаточно золота с собой для отправки в банк."
    else:
        SQLighter.set_gold(db, user_id, chat_id, current_gold - money)
        SQLighter.set_bank_gold(db, user_id, chat_id, current_bank_gold + money)
        SQLighter.restore_today_caravan_available(db, user_id, 0)
        return f"{money} золота отправлено в банк. Золота в банке: {current_bank_gold + money}. Золота с собой: {current_gold - money}"

def transfer_to_bank_all(user_id, chat_id):
    current_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
    current_bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, user_id, chat_id)[0])
    if current_gold < 1:
        return "Недостаточно золота с собой для отправки в банк."
    else:
        SQLighter.set_gold(db, user_id, chat_id, 0)
        SQLighter.set_bank_gold(db, user_id, chat_id, current_bank_gold + current_gold)
        SQLighter.restore_today_caravan_available(db, user_id, 0)
        return f"Всё золото отправлено в банк. Сейчас золота в банке: {current_bank_gold + current_gold}"

def go_work(user_id, chat_id):
    today_caravan_available = int_from_db_answer(SQLighter.get_today_caravan_available(db, user_id, chat_id)[0])
    if today_caravan_available < 5:
        return "Вы на сегодня слишком вымотаны, чтобы идти на работу.", False
    else:
        SQLighter.set_today_caravan_available(db, user_id, chat_id, 0)
        current_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
        SQLighter.set_gold(db, user_id, chat_id, current_gold + 50)
        answer = "Опять работа? Ну, ладно. Жить на что-то же надо... держи свои 50 золотых.\n"
        build = buildings[dialogs.get_random_int(0, len(buildings)-1)]
        try:
            current_progress = int_from_db_answer(SQLighter.get_build_progress(db, chat_id, build)[0])
        except:
            SQLighter.add_new_builder_status(db, chat_id)
            current_progress = 0
        if current_progress + 1 < 100:
            SQLighter.set_build_progress(db, chat_id, build, current_progress + 1)
            answer += f"\nСегодня тебя отправили на строительство {buildings_list[build]}.\nПрогресс строительства: {current_progress + 1} из 100"
        else:
            SQLighter.set_build_progress(db, chat_id, build, 0)
            users = SQLighter.get_users_list_from_chat(db, chat_id)
            if build == "temple":
                answer += "\nНарод ликует - достроен очередной храм в городе!\nНо его ещё надо обустроить, так что со всех, у кого есть золото, принудительно берётся абсолютно добровольный взнос в 10% от всего накопленного."
                for user in users:
                    current_user_id = int_from_db_answer(user[0])
                    current_user_gold = int_from_db_answer(SQLighter.get_gold(db, current_user_id, chat_id)[0])
                    current_user_bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, current_user_id, chat_id)[0])
                    if current_user_gold > 10:
                        SQLighter.set_gold(db, current_user_id, chat_id, round(current_user_gold / 10) * 9)
                    if current_user_bank_gold > 10:
                        SQLighter.set_bank_gold(db, current_user_id, chat_id, round(current_user_bank_gold / 10) * 9)
            if build == "casino":
                answer += "\nВсе жители города в предвкушении - открылся очередной игорный дом!\nКонечно же, никто из чата, у кого есть с десяток золотых с собой в кармане, не прошёл мимо и попытал удачу."
                for user in users:
                    current_user_id = int_from_db_answer(user[0])
                    current_username = str_from_db_answer(SQLighter.get_username_by_id(db, current_user_id)[0])
                    current_title = get_user_title(current_user_id, chat_id).capitalize()
                    current_user_gold = int_from_db_answer(SQLighter.get_gold(db, current_user_id, chat_id)[0])
                    if current_user_gold > 10:
                        roulette_casino = dialogs.get_random_int(0, 101)
                        if roulette_casino < 21:
                            answer += f"\n- {current_title} {current_username} бросил вызов казино, но проиграл все деньги."
                            SQLighter.set_gold(db, current_user_id, chat_id, 0)
                        if roulette_casino > 20 and roulette_casino < 61:
                            answer += f"\n- {current_title} {current_username} бросил вызов казино, но проиграл половину своих денег."
                            SQLighter.set_gold(db, current_user_id, chat_id, round(current_user_gold / 2))
                        if roulette_casino > 60 and roulette_casino < 91:
                            answer += f"\n- {current_title} {current_username} бросил вызов казино и вышел победителем, увеличив свой капитал."
                            SQLighter.set_gold(db, current_user_id, chat_id, current_user_gold + round(current_user_gold / 2))
                        if roulette_casino > 90:
                            answer += f"\n- {current_title} {current_username} сорвал джек-пот! Он вынес из казино в 3 раза больше, чем.взял тудо с собой."
                            SQLighter.set_gold(db, current_user_id, chat_id, current_user_gold * 3)
            if build == "fair":
                answer += "\nСегодня у жителей города праздник - наконец подготовление к ярморке завершены!\nЯрмарка проходит красочно, а всем участникам чата выплачивается по 200 золотых в подарок за участие."
                for user in users:
                    current_user_id = int_from_db_answer(user[0])
                    current_user_gold = int_from_db_answer(SQLighter.get_gold(db, current_user_id, chat_id)[0])
                    SQLighter.set_gold(db, current_user_id, chat_id, current_user_gold + 200)
        return answer, True

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
    answer = str_from_db_answer(db_answer)
    if (answer == ""):
        return 0
    else:
        return int(answer)

# Функция для преобразования ответа от БД в строку.
def str_from_db_answer(db_answer):
    return str(db_answer).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "").strip()

def get_mystery_dialog():
    return dialogs.get_mystery_dialog()

# Случайное событие в чате
def get_random_event(user_id, chat_id):
    answer = check_is_admin(user_id, chat_id)
    if (answer != ""):
        return answer
    answer = "Боги хаоса были призваны в этот мир!\n"
    event = random_events[dialogs.get_random_int(1, len(random_events)-1)]
    user_list = SQLighter.get_users_list_from_chat(db, chat_id)
    rand_user_id = int_from_db_answer(user_list[dialogs.get_random_int(0, len(user_list)-1)])
    username = str_from_db_answer(SQLighter.get_username_by_id(db, rand_user_id)[0])
    user_title = get_user_title(rand_user_id, chat_id)
    to_user = "@{}".format(username)
    if (event == "add_free_rep"):
        rand_free_rep = dialogs.get_random_int(1, 10)
        restore_free_rep_for_user(user_id, to_user, chat_id, rand_free_rep)
        answer += "Богам не хватает веселья. Они дарят доступные очки действий в размере {} для {} {}. Пользуйся этим даром с умом.".format(rand_free_rep, user_title, username)
        return answer
    if (event == "lose_free_rep"):
        rand_free_rep = 0 - dialogs.get_random_int(1, 10)
        restore_free_rep_for_user(user_id, to_user, chat_id, rand_free_rep)
        answer += "Боги на сегодня устали. Щелчком пальцев, {} {} теряет очки действий в размере {}.".format(user_title, username, rand_free_rep)
        return answer
    if (event == "add_rep"):
        rand_rep = dialogs.get_random_int(1, 10)
        current_rep = int_from_db_answer(SQLighter.get_rep(db, rand_user_id, chat_id)[0])
        current_rep_pos_offset = int_from_db_answer(SQLighter.get_rep_pos_offset(db, rand_user_id, chat_id)[0])
        SQLighter.change_rep(db, rand_user_id, chat_id, current_rep + rand_rep)
        SQLighter.change_pos_rep(db, rand_user_id, chat_id, current_rep_pos_offset + rand_rep)
        answer += "Боги шумно веселятся. Им явно понравился {} {}, так что его репутация растёт! Он получил повышение репутации в размере {}.".format(user_title, username, rand_rep)
        return answer
    if (event == "lose_rep"):
        rand_rep = 0 - dialogs.get_random_int(1, 10)
        current_rep = int_from_db_answer(SQLighter.get_rep(db, rand_user_id, chat_id)[0])
        current_rep_pos_offset = int_from_db_answer(SQLighter.get_rep_pos_offset(db, rand_user_id, chat_id)[0])
        SQLighter.change_rep(db, rand_user_id, chat_id, current_rep + rand_rep)
        SQLighter.change_pos_rep(db, rand_user_id, chat_id, current_rep_pos_offset + rand_rep)
        answer += "Боги гневаются. А первым попался им под руку {} {}. Бедняга получет на свою голову понижение репутации в размере {}.".format(user_title, username, rand_rep)
        return answer
    if event == "add_gold":
        rand_gold = dialogs.get_random_int(1, 200)
        current_gold = int_from_db_answer(SQLighter.get_gold(db, rand_user_id, chat_id)[0])
        SQLighter.set_gold(db, rand_user_id, chat_id, current_gold + rand_gold)
        answer += "Боги щедрятся. Они осыпают золотом {} {}. Прибыль составила {} золотых.".format(user_title, username, rand_gold)
        return answer
    if event == "lose_gold":
        rand_gold = 0 - dialogs.get_random_int(1, 200)
        current_gold = int_from_db_answer(SQLighter.get_gold(db, rand_user_id, chat_id)[0])
        if current_gold < rand_gold:
            rand_gold -= current_gold
            SQLighter.set_gold(db, rand_user_id, chat_id, 0)
            current_bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, rand_user_id, chat_id)[0])
            if current_bank_gold < rand_gold:
                SQLighter.set_bank_gold(db, rand_user_id, chat_id, 0)
                answer += "Завистливые боги не могут спокойно смотреть на золото, накопленное у {} {}. По щелчку их пальцев всё золото превратилось в странного цвета жижу.".format(user_title, username)
                return answer
            else:
                SQLighter.set_bank_gold(db, rand_user_id, chat_id, current_bank_gold - rand_gold)
        else:
            SQLighter.set_gold(db, rand_user_id, chat_id, current_gold - rand_gold)
        answer += "Завистливые боги не могут спокойно смотреть на золото, накопленное у {} {}. По щелчку их пальцев {} золотых превратилось в странного цвета жижу.".format(user_title, username, -rand_gold)
        return answer
    answer += "Но, кажется, сейчас они не в настроении что-то делать."
    return answer

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

# Бой против игрока
def fight_with_player(from_user, to_user, chat_id):
    free_rep = int_from_db_answer(SQLighter.get_free_rep(db, from_user, chat_id)[0])
    if (free_rep < 2):
        return "Не хватает доступных очков действий!\nНужно очков: 2\nДоступно очков: {}".format(free_rep)
    to_username = check_and_get_username(to_user)
    to_user_id = int_from_db_answer(SQLighter.get_id_by_username(db, to_username)[0])
    from_username = str_from_db_answer(SQLighter.get_username_by_id(db, from_user)[0])
    from_username_title = get_user_title(from_user, chat_id).title()
    to_username_title = get_user_title(to_user_id, chat_id)
    answer = "Внимание, зафиксирован бросок кубика!\n"
    if (from_user != to_user_id):
        i = dialogs.get_random_int(1, 6)
        dice_mod = str_from_db_answer(SQLighter.get_dice_mod(db, from_user, chat_id)[0])
        add_sum_dice = int(dice_mod[1])
        add_dice = int(dice_mod[3])
        if add_sum_dice > 0:
            i += add_sum_dice
            answer += f"{from_username_title} {from_username} умело использует подкрутку и увеличивает результат своего броска кубика на {add_sum_dice}.\n"
        if add_dice > 0:
            while add_dice > 0:
                j = dialogs.get_random_int(1, 6)
                i += j
                answer += f"{from_username_title} {from_username} обходит правила и кидает ещё один кубик. Выпадает {j}.\n"
                add_dice -= 1
        SQLighter.change_free_rep(db, from_user, chat_id, free_rep - 2)
        current_immune_days = int_from_db_answer(SQLighter.get_immune_days(db, to_user_id, chat_id)[0])
        if current_immune_days > 0:
            answer += f"{from_username_title} {from_username} пытается напасть на {to_username_title} {to_username}, но в дело вмешиваются мистические силы. Атака провалилась, но зато боевая слава участников не пострадала."
            return answer
        battle_glory_offset = 1
        if (i < 4):
            lose = "Неудача!"
            if (i == 1):
                battle_glory_offset = 2
                lose = "Критическая неудача!"
            change_battle_glory(from_user, chat_id, 0 - battle_glory_offset)
            change_battle_glory(to_user_id, chat_id, battle_glory_offset)
            current_battle_glory_from = int_from_db_answer(SQLighter.get_battle_glory(db, from_user, chat_id)[0])
            current_battle_glory_to = int_from_db_answer(SQLighter.get_battle_glory(db, to_user_id, chat_id)[0])
            answer += "\nРезультат броска: {} из 6. {}\n\n{} {} {}\nБоевая слава нападающего: {} (-{}).\nБоевая слава жертвы: {} (+{}).".format(i, lose, from_username_title, from_username, dialogs.get_fight_dialog(False), current_battle_glory_from, battle_glory_offset, current_battle_glory_to, battle_glory_offset)
        else:
            win = "Удача!"
            if (i >= 6):
                battle_glory_offset = 2
                win = "Критическая удача!"
            change_battle_glory(from_user, chat_id, battle_glory_offset)
            change_battle_glory(to_user_id, chat_id, 0 - battle_glory_offset)
            current_battle_glory_from = int_from_db_answer(SQLighter.get_battle_glory(db, from_user, chat_id)[0])
            current_battle_glory_to = int_from_db_answer(SQLighter.get_battle_glory(db, to_user_id, chat_id)[0])
            answer += "\nРезультат броска: {} из 6. {}\n\n{} {} {} {} {}.\nБоевая слава нападающего: {} (+{}).\nБоевая слава жертвы: {} (-{}).".format(i, win, from_username_title, from_username, dialogs.get_fight_dialog(True), to_username_title, to_username, current_battle_glory_from, battle_glory_offset, current_battle_glory_to, battle_glory_offset)
    else:
        answer = "{} {} {}".format(from_username_title, from_username, dialogs.get_fight_against_yourself_dialog())
    return answer

# Изменение боевой славы
def change_battle_glory(user_id, chat_id, battle_glory):
    current_battle_glory = int_from_db_answer(SQLighter.get_battle_glory(db, user_id, chat_id)[0])
    current_battle_glory_offset = int_from_db_answer(SQLighter.get_battle_glory_offset(db, user_id, chat_id)[0])
    SQLighter.change_battle_glory(db, user_id, chat_id, current_battle_glory + battle_glory)
    SQLighter.change_battle_glory_offset(db, user_id, chat_id, current_battle_glory_offset + battle_glory)

def get_user_id_by_username(username):
    return int_from_db_answer(SQLighter.get_id_by_username(db, username)[0])

# Рулетка
def roulette(user_id, chat_id):
    answer = ""
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    username_title = get_user_title(user_id, chat_id)
    new_game = False
    if (int_from_db_answer(SQLighter.check_dead_user(db, user_id, chat_id)[0]) < 1):
        return "Играть в рулетку с мертвецами не интересно. Воскрешайся и приходи завтра!", False
    try:
        last_rw = last_winner[chat_id]
    except:
        last_rw = ""
    try:
        roulette_current_bullets = chat_games[chat_id]
        roulette_current_bullets += 1
        chat_games[chat_id] = roulette_current_bullets
        current_revolver_drum = revolvers[chat_id]
        while True:
            bullet = dialogs.get_random_int(0, 5)
            if (current_revolver_drum[bullet] != 0):
                continue
            else:
                current_revolver_drum[bullet] = 1
                break
        revolvers[chat_id] = current_revolver_drum
    except:
        if (int_from_db_answer(SQLighter.get_free_roulette(db, user_id, chat_id)[0]) < 1):
            return "На сегодня попытки игры в рулетку у вас израсходованы. Возвращайтесь завтра!", False
        new_game = True
        chat_games[chat_id] = 1
        roulette_current_bullets = 1
        current_revolver_drum = [0, 0, 0, 0, 0, 0]
        current_revolver_drum[dialogs.get_random_int(0, 5)] = 1
        revolvers[chat_id] = current_revolver_drum
    if (new_game):
        SQLighter.change_roulette_today(db, user_id, chat_id)

    boom = dialogs.get_random_int(0, 5)
    drum = get_drum(current_revolver_drum, boom)
    boom_result = current_revolver_drum[boom] == 1
    if (boom_result):
        current_roulette_lose = int_from_db_answer(SQLighter.get_roulette_lose(db, user_id, chat_id)[0])
        SQLighter.change_roulette_lose(db, user_id, chat_id, current_roulette_lose + 1)
        SQLighter.change_roulette_today(db, user_id, chat_id)
        SQLighter.zero_free_roulette(db, user_id, chat_id)
        chat_games.pop(chat_id)
        revolvers.pop(chat_id)
        if (last_rw != ""):
            last_winner.pop(chat_id)
        answer += "БА-БАХ!\n[{}]".format(drum)
    else:
        current_roulette_win = int_from_db_answer(SQLighter.get_roulette_win(db, user_id, chat_id)[0])
        SQLighter.change_roulette_win(db, user_id, chat_id, current_roulette_win + 1)
        last_winner[chat_id] = username
        if (roulette_current_bullets < 5):
            change_battle_glory(user_id, chat_id, roulette_current_bullets * 2)
            answer += "ЩЁЛК!\n[{}]".format(drum)
        else:
            change_battle_glory(user_id, chat_id, roulette_current_bullets * 3)
            answer += "ЩЁЛК!\n[{}]".format(drum)
            chat_games.pop(chat_id)
            revolvers.pop(chat_id)
            last_winner.pop(chat_id)
    return answer, boom_result

def get_drum(drum, bullet):
    drum_list = ""
    i = 0
    while (i < 6):
        if (drum[i] == 1):
            if (bullet == i):
                drum_list += "💥"
            else:
                drum_list += "⚫️"
        else:
            if (bullet == i):
                drum_list += "🟢"
            else:
                drum_list += "⚪️"
        i += 1
    return drum_list

def stop_roulette(user_id, chat_id):
    try:
        last_rw = last_winner[chat_id]
    except:
        last_rw = ""
    chat_games.pop(chat_id)
    revolvers.pop(chat_id)
    if (last_rw != ""):
        last_winner.pop(chat_id)
    change_battle_glory(user_id, chat_id, -5)
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    username_title = get_user_title(user_id, chat_id)
    return "{} {} жертвует 5 очков боевой славы чтобы разрядить пистолет.".format(username_title.title(), username)

def roll(user_id, chat_id):
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    username_title = get_user_title(user_id, chat_id)
    return "{} {} бросает кубик. Выпадает {}.".format(username_title.capitalize(), username, dice(1,6))

def dice(start, finish):
    return dialogs.get_random_int(start, finish)

def restore_standard_daily_params():
    unique_users = []
    user_list = SQLighter.get_users_list(db)
    for user_id_from_bd in user_list:
        user_id = int_from_db_answer(user_id_from_bd)
        if user_id not in unique_users:
            unique_users.append(user_id)
    for user_id in unique_users:
        SQLighter.restore_free_rep(db, user_id, 10)
        SQLighter.restore_neg_and_pos_rep(db, user_id)
        SQLighter.restore_free_roulette(db, user_id)
        SQLighter.restore_roulette_today(db, user_id)
        SQLighter.restore_battle_glory_offset(db, user_id)
        SQLighter.restore_today_caravan_available(db, user_id, 5)
        SQLighter.restore_dice_mod(db, user_id)
        current_immune = SQLighter.get_immune_days_all_chat_by_user(db, user_id)
        for immune in current_immune:
            day = int_from_db_answer(immune[0])
            immune_chat_id = int_from_db_answer(immune[1])
            if day > 0:
                SQLighter.set_immune_days(db, user_id, immune_chat_id, day - 1)
        current_admin = SQLighter.get_admin_days_all_chat_by_user(db, user_id)
        for admin in current_admin:
            day = int_from_db_answer(admin[0])
            admin_chat_id = int_from_db_answer(admin[1])
            if day > 0:
                SQLighter.set_admin_days(db, user_id, admin_chat_id, day - 1)
                if day - 1 == 0:
                    SQLighter.set_admin(db, user_id, admin_chat_id, 0)
                else:
                    SQLighter.set_admin(db, user_id, admin_chat_id, 1)
        current_bank_gold = SQLighter.get_bank_gold_all_chat_by_user(db, user_id)
        for bank_gold in current_bank_gold:
            gold = int_from_db_answer(bank_gold[0])
            bank_chat_id = int_from_db_answer(bank_gold[1])
            if gold > 10:
                SQLighter.set_bank_gold(db, user_id, bank_chat_id, gold - 10)
            else:
                SQLighter.set_bank_gold(db, user_id, bank_chat_id, 0)
                current_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, bank_chat_id))
                SQLighter.set_gold(db, user_id, bank_chat_id, current_gold + gold)

def test():
    print("Hello")

def service_work(gold):
    user_list = SQLighter.get_users_list(db)
    for user_id_from_bd in user_list:
        user_id = int_from_db_answer(user_id_from_bd)
        current_bank_gold = SQLighter.get_bank_gold_all_chat_by_user(db, user_id)
        for bank_gold in current_bank_gold:
            current_gold = int_from_db_answer(bank_gold[0])
            bank_chat_id = int_from_db_answer(bank_gold[1])
            SQLighter.set_bank_gold(db, user_id, bank_chat_id, current_gold + int(gold))
    return "Рассылка завершена!", get_all_chat_ids()

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
        activity += int_from_db_answer(user_activity_from_bd[0])
    return activity

def get_user_activity(user_id, chat_id):
    user_activity = int_from_db_answer(SQLighter.get_user_activity(db, user_id, chat_id)[0])
    all_activity = get_all_activity(chat_id)
    if (all_activity != 0):
        return round(user_activity / all_activity * 100, 2)
    else:
        return "Активность в чате отсуствует"

def get_my_top(user_id, username, chat_id):
    user_title = get_user_title(user_id, chat_id)
    answer = "Топ {} {}:\n\n".format(user_title, username)
    answer += get_user_top_message(user_id, chat_id, True)
    answer += get_user_top_rep(user_id, chat_id, True)
    answer += get_user_top_act(user_id, chat_id, True)
    answer += get_user_top_fg(user_id, chat_id, True)
    answer += get_user_top_pirate(user_id, chat_id, True)
    return answer

def get_my_gold(user_id, chat_id):
    current_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id))
    current_bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, user_id, chat_id))
    return f"Всего золота: {current_gold + current_bank_gold}\nЗолото с собой: {current_gold}\nЗолото в банке: {current_bank_gold}"
    
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

def get_top_active(user_id, chat_id, count):
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
        count_act = ""
        if (count > 0):
            count_act = "-{}".format(count)
        top_act_list = SQLighter.get_top_act_list(db, chat_id, count)
        all_activity = get_all_activity(chat_id)
        answer = "Топ{} по активности:\n".format(count_act)
        i = 1
        for top_user in top_act_list:
            user_and_act = str_from_db_answer(top_user).split(" ")
            user_id = user_and_act[0]
            username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
            act_count = round(int_from_db_answer(user_and_act[1]) / all_activity * 100, 2)
            answer += "{}. {} {}. Активность: {}%\n".format(i, get_user_title(user_id, chat_id).title(), username, act_count)
            i += 1
        return answer
    else:
        return get_user_top_act(to_user, chat_id, False)

def get_top_fight(user_id, chat_id, count):
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
        count_fg = ""
        if (count > 0):
            count_fg = "-{}".format(count)
        top_fg_list = SQLighter.get_top_fg_list(db, chat_id, count)
        answer = "Топ{} по боевой славе:\n".format(count_fg)
        i = 1
        for top_user in top_fg_list:
            user_and_fg = str_from_db_answer(top_user).split(" ")
            user_id = user_and_fg[0]
            username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
            fg_count = user_and_fg[1]
            answer += "{}. {} {}. Боевая слава: {}\n".format(i, get_user_title(user_id, chat_id).title(), username, fg_count)
            i += 1
        return answer
    else:
        return get_user_top_fg(to_user, chat_id, False)

def get_top_pirate(user_id, chat_id, count):
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
        count_pirate = ""
        if (count > 0):
            count_pirate = "-{}".format(count)
        top_pirates = SQLighter.get_top_pirate_list(db, chat_id)
        top_pirate_list = []
        for user in top_pirates:
            top_pirate_list.append((user[0], user[1] + user[2]))
        top_pirate_list = sorted(top_pirate_list, key=itemgetter(1), reverse=True)
        if count != 0:
            top_pirate_list = top_pirate_list[0:count]
        else:
            top_pirate_list = top_pirate_list
        answer = "Топ{} по накопленному золоту:\n".format(count_pirate)
        i = 1
        for top_user in top_pirate_list:
            user_and_pirate = str_from_db_answer(top_user).split(" ")
            user_id = user_and_pirate[0]
            username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
            pirate_count = user_and_pirate[1]
            answer += "{}. {} {}. Накоплено золота: {}\n".format(i, get_user_title(user_id, chat_id).title(), username, pirate_count)
            i += 1
        return answer
    else:
        return get_user_top_pirate(to_user, chat_id, False)

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

def get_user_top_act(user_id, chat_id, my_stat):
    top_act_list = SQLighter.get_top_act_list(db, chat_id, 0)
    user_act = get_user_activity(user_id, chat_id)
    if (type(user_act) != float):
        return user_act
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    i = 1
    answer = "{}, тебя нет в топе. Обратись к администратору бота.".format(username)
    if (my_stat):
        for top_user in top_act_list:
            user_and_act = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_act[0])):
                answer = "Активность: {}%\nРанг в топе по активности: {}\n".format(user_act, i)
            i += 1
    else:
        for top_user in top_act_list:
            user_and_act = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_act[0])):
                answer = "{} {}.\nАктивность: {}%\nРанг в топе: {}\n".format(get_user_title(user_id, chat_id).title(), username, user_act, i)
            i += 1
    return answer

def get_user_top_fg(user_id, chat_id, my_stat):
    top_fg_list = SQLighter.get_top_fg_list(db, chat_id, 0)
    user_fg = int_from_db_answer(SQLighter.get_battle_glory(db, user_id, chat_id)[0])
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    i = 1
    answer = "{}, тебя нет в топе. Обратись к администратору бота.".format(username)
    if (my_stat):
        for top_user in top_fg_list:
            user_and_fg = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_fg[0])):
                answer = "Боевая слава: {}\nРанг в топе по боевой славе: {}\n".format(user_fg, i)
            i += 1
    else:
        for top_user in top_fg_list:
            user_and_fg = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_fg[0])):
                answer = "{} {}.\Боевая слава: {}\nРанг в топе: {}\n".format(get_user_title(user_id, chat_id).title(), username, user_fg, i)
            i += 1
    return answer

def get_user_top_pirate(user_id, chat_id, my_stat):
    top_pirates = SQLighter.get_top_pirate_list(db, chat_id)
    top_pirate_list = []
    for user in top_pirates:
        top_pirate_list.append((user[0], user[1] + user[2]))
    top_pirate_list = sorted(top_pirate_list, key=itemgetter(1), reverse=True)
    hand_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
    bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, user_id, chat_id)[0])
    user_gold = hand_gold + bank_gold
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    i = 1
    answer = "{}, тебя нет в топе. Обратись к администратору бота.".format(username)
    if my_stat:
        for top_user in top_pirate_list:
            user_and_pirate = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_pirate[0])):
                answer = "Накоплено золота: {}\nРанг в топе по накопленному золоту: {}\n".format(user_gold, i)
            i += 1
    else:
        for top_user in top_pirate_list:
            user_and_pirate = str_from_db_answer(top_user).split(" ")
            if (user_id == int(user_and_pirate[0])):
                answer = "{} {}.\Накоплено золота: {}\nРанг в топе: {}\n".format(get_user_title(user_id, chat_id).title(), username, user_gold, i)
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

def get_all_chat_ids():
    chat_id_list = []
    ids = SQLighter.get_chat_ids(db)
    if (len(ids) > 0):
        for chat_id in ids:
            chat_id_list.append(int_from_db_answer(chat_id))
    return chat_id_list

def get_fight_top(chat_id):
    user_id = int_from_db_answer(SQLighter.get_fight_top(db, chat_id)[0])
    battle_glory_offset = int_from_db_answer(SQLighter.get_battle_glory_offset(db, user_id, chat_id)[0])
    if (battle_glory_offset != 0):
        return "{} {}.\nПоказатель боевой славы за сегодня: {}".format(get_user_title(user_id, chat_id).title(), str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]), battle_glory_offset)
    else:
        return ""

def get_fight_loser(chat_id):
    user_id = int_from_db_answer(SQLighter.get_fight_loser(db, chat_id)[0])
    battle_glory_offset = int_from_db_answer(SQLighter.get_battle_glory_offset(db, user_id, chat_id)[0])
    if (battle_glory_offset != 0):
        return "{} {}.\nПоказатель боевой славы за сегодня: {}".format(get_user_title(user_id, chat_id).title(), str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]), battle_glory_offset)
    else:
        return ""

def magic_ball(user_id, chat_id, question):
    if question == "":
        return ""
    ball_answer = dialogs.get_magic_ball_dialog()
    username = str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0])
    user_title = get_user_title(user_id, chat_id).capitalize()
    return "{} {} трясёт шар судьбы и задаёт вопрос: {}\n\nШар судьбы отвечает: {}".format(user_title, username, question, ball_answer)

# Формирование статуса.
def status_by_user(user_id, chat_id):
    line = "_____________________"
    CR = "\n"
    result_text = line + CR
    name = "Имя: {}".format(str_from_db_answer(SQLighter.get_username_by_id(db, user_id)[0]))
    result_text += name + CR
    title = "Титул: {}".format(get_user_title(user_id, chat_id).title())
    result_text += title + CR
    roulette_wins = "Оставался жив в передаче \"Русская рулетка\": {}".format(int_from_db_answer(SQLighter.get_roulette_win(db, user_id, chat_id)[0]))
    result_text += roulette_wins + CR
    roulette_loses = "Смертей в передаче \"Русская рулетка\": {}".format(int_from_db_answer(SQLighter.get_roulette_lose(db, user_id, chat_id)[0]))
    result_text += roulette_loses + CR + CR
    activity = get_user_top_act(user_id, chat_id, True)
    result_text += activity
    messages = get_user_top_message(user_id, chat_id, True)
    result_text += messages
    rep = get_user_top_rep(user_id, chat_id, True)
    result_text += rep
    fg = get_user_top_fg(user_id, chat_id, True)
    result_text += fg
    pirate = get_user_top_pirate(user_id, chat_id, True)
    result_text += pirate
    free_rep = "Очков действий: {}".format(int_from_db_answer(SQLighter.get_free_rep(db, user_id, chat_id)[0]))
    result_text += free_rep + CR
    current_battle_glory = "Боевая слава: {}".format(int_from_db_answer(SQLighter.get_battle_glory(db, user_id, chat_id)[0]))
    result_text += current_battle_glory + CR
    hand_gold = int_from_db_answer(SQLighter.get_gold(db, user_id, chat_id)[0])
    bank_gold = int_from_db_answer(SQLighter.get_bank_gold(db, user_id, chat_id)[0])
    user_gold = hand_gold + bank_gold
    current_gold = f"Накоплено золота: {user_gold}"
    result_text += current_gold + CR
    status = result_text + line
    return status

def get_all_dead(chat_id):
    dead_list = []
    deads = SQLighter.get_all_dead_in_chat(db, chat_id)
    if (len(deads) > 0):
        for dead_id_from_db in deads:
            dead_id = int_from_db_answer(dead_id_from_db)
            full_name = "{} {}".format(get_user_title(dead_id, chat_id).capitalize(), str_from_db_answer(SQLighter.get_username_by_id(db, dead_id)[0]))
            dead_list.append("● " + full_name)
    return dead_list

def get_help(user_id, chat_id):
    admin = True
    check_admin = check_is_admin(user_id, chat_id)
    if (check_admin != ""):
        admin = False
    command_list = "Список доступных команд:\n"
    command_list += "● /top_my - вызов своей статистики только по топам\n"
    command_list += "● /stat - вызов своей общей статистики\n"
    command_list += "● \"+\" или \"-\" в ответ на сообщение другого пользователя - изменение репутации пользователя\n"
    command_list += "● /main_pos - кто сегодня собрал больше всех плюсов?\n"
    command_list += "● /main_neg - кто сегодня собрал больше всех минусов?\n"
    command_list += "● /fight [username] - вызов игроку с броском кубика. При удаче - урон по боевой славе оппонента и поднятие своей боевой славы, при неудаче - урон своей боевой славе.\n"
    command_list += "● /roulette - передача \"Русская рулетка\".\n"
    command_list += "● /roulette_stat - проверка текущего количества патронов в стволе.\n"
    command_list += "● /stop_roulette - разрядить рулетку за 5 единиц боевой славы.\n"
    command_list += "● /roll - кинуть кубик\n"
    command_list += "● /magic_ball - попросить совет у шара предсказаний"
    if (admin):
        command_list += "\n● /add_free_rep [username] [count] - добавить свободные очки репутации (count) пользователю (username)\n"
        command_list += "● /top_message [username / count] - вызов топа по сообщениям у конкретного пользователя (username) или по количеству (count)\n"
        command_list += "● /top_rep [username / count] - вызов топа по репутации у конкретного пользователя (username) или по количеству (count)\n"
        command_list += "● /top_act [username / count] - вызов топа по активности у конкретного пользователя (username) или по количеству (count)\n"
        command_list += "● /top_fight [username / count] - вызов топа по боевой славе у конкретного пользователя (username) или по количеству (count)\n"
        command_list += "● /assign_title [username] [title] - добавить титул (title) пользователю (username)\n"
        command_list += "● /random - вызов случайного события для конференции"
    return command_list

def get_help_PM():
    command_list = "Список доступных команд (без команд администратора):\n"
    command_list += "● /top_my - вызов своей статистики только по топам\n"
    command_list += "● /stat - вызов своей общей статистики\n"
    command_list += "● \"+\" или \"-\" в ответ на сообщение другого пользователя - изменение репутации пользователя"
    command_list += "● /main_pos - кто сегодня собрал больше всех плюсов?\n"
    command_list += "● /main_neg - кто сегодня собрал больше всех минусов?\n"
    command_list += "● /fight [username] - вызов игроку с броском кубика. При удаче - урон по боевой славе оппонента и поднятие своей боевой славы, при неудаче - урон своей боевой славе.\n"
    command_list += "● /roulette - передача \"Русская рулетка\".\n"
    command_list += "● /roulette_stat - проверка текущего количества патронов в стволе.\n"
    command_list += "● /stop_roulette - разрядить рулетку за 5 единиц боевой славы.\n"
    command_list += "● /roll - кинуть кубик\n"
    command_list += "● /magic_ball - попросить совет у шара предсказаний"
    return command_list