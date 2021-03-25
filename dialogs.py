import random

def get_random_int(start, finish):
    return random.randint(start, finish)

def get_fight_dialog(result):
    if (result):
        i = random.randint(0, len(fight_pos_list())-1)
        return fight_pos_list()[i]
    else:
        i = random.randint(0, len(fight_neg_list())-1)
        return fight_neg_list()[i]

def get_fight_against_yourself_dialog():
    i = random.randint(0, len(fight_yourself_list())-1)
    return fight_yourself_list()[i]

def get_cause_of_death():
    i = random.randint(0, len(cause_of_death_list())-1)
    return cause_of_death_list()[i]

def get_fight_top():
    i = random.randint(0, len(fight_top_list())-1)
    return fight_top_list()[i]

def get_fight_loser():
    i = random.randint(0, len(fight_loser_list())-1)
    return fight_loser_list()[i]

def fight_pos_list():
    fight_list = []
    fight_list.append("с размаху бьёт киркой")
    fight_list.append("кидает перчаткой в лицо")
    fight_list.append("делает кусь")
    fight_list.append("вызывает на дуэль и побеждает")
    fight_list.append("насмехается над")
    fight_list.append("бьёт по лицу")
    fight_list.append("выполнил идеальный гоп-стоп для")
    fight_list.append("с первой же раздачи карт собрал флеш рояль во время в покер игры с")
    return fight_list

def fight_neg_list():
    fight_list = []
    fight_list.append("замахивается дубиной, но подскальзывается на банановой кожуре.")
    fight_list.append("стреляет в противника, но попадает себе в ногу.")
    fight_list.append("готовит ловушку, но по глупости сам попадает в неё.")
    fight_list.append("вызывает оппонента на дуэль, но сегодня он слишком похож на известного Александра Сергеевича.")
    fight_list.append("понимает, что он не Мюнхаузен, а стрелять собой из пушки по противнику не лучшая идея.")
    fight_list.append("очень плохо шутит над противником, вызывая только насмешки над самим собой.")
    fight_list.append("хочет играть в роли Бэтмена, но почему-то всегда оказывается в роли избитого Джокера.")
    fight_list.append("вызывает на помощь Администратора Бота, но делает это без уважения.")
    return fight_list

def fight_yourself_list():
    fight_list = []
    fight_list.append("пытается прогнать голоса в голове и бьётся об стену головой.")
    fight_list.append("изучает химию, пробуя на вкус образцы.")
    fight_list.append("играет в ассасинов и делает прыжок веры. Правда, всё сено уже увезли.")
    fight_list.append("пытается получить премию Дарвина.")
    fight_list.append("решает взять пару приёмов для охоты у льва, запрыгнув в вольер зоопарка.")
    fight_list.append("испытывает себя восхождением на Эверест. В одиночку. Без снаряжения.")
    fight_list.append("пытается выучить латынь, но снова призывает демонов.")
    fight_list.append("хочет сыграть в рулетку, но из оружия есть только ПМ.")
    return fight_list

def cause_of_death_list():
    cause_list = []
    cause_list.append("пустил пулю себе в лоб. Странно, вроде так не играют в рулетку...")
    cause_list.append("испугался выстрела до смерти.")
    cause_list.append("\"высокое содержание свинца в мозгу\", как заявил наш эксперт.")
    cause_list.append("забыл указать в контракте с Дьяволом неуязвимость к пулям.")
    cause_list.append("решил, что даже если проиграет, у него будет второй шанс. Наивный.")
    cause_list.append("умер от старости. Шутка. От пулевого ранения в голову.")
    return cause_list

def fight_top_list():
    fight_top = []
    fight_top.append("главный гопник на районе")
    fight_top.append("нанёс своим противникам чуть более, чем over9000 урона")
    fight_top.append("критовал так, что весь чат стоял на ушах")
    fight_top.append("показал остальным, кто тут босс качалки")
    fight_top.append("поиграл с остальными в БДСМ, но исключительно в роли садиста")
    return fight_top

def fight_loser_list():
    fight_loser = []
    fight_loser.append("самое слабое звено.")
    fight_loser.append("ловил лицом все подачи.")
    fight_loser.append("сражался хоть и храбро, но закончил всё равно бесславно.")
    fight_loser.append("отлично сыграл роль груши для битья.")
    fight_loser.append("главная жертва кибербуллинга.")
    return fight_loser