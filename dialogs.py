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

def fight_pos_list():
    fight_list = []
    fight_list.append("с размаху бьёт киркой")
    fight_list.append("кидает перчаткой в лицо")
    fight_list.append("делает кусь")
    fight_list.append("вызывает на дуэль и побеждает")
    return fight_list

def fight_neg_list():
    fight_list = []
    fight_list.append("замахивается дубиной, но подскальзывается на банановой кожуре.")
    fight_list.append("берёт в прицел оппонента и стреляет, но попадает себе в ногу.")
    fight_list.append("готовит ловушку, но по глупости сам попадает в неё.")
    fight_list.append("вызывает оппонента на дуэль, но сегодня он слишком похож на известного Александра Сергеевича.")
    return fight_list

def fight_yourself_list():
    fight_list = []
    fight_list.append("пытается прогнать голоса в голове и бьётся об стену головой.")
    fight_list.append("изучает химию, пробуя на вкус образцы.")
    fight_list.append("играет в ассасинов и делает прыжок веры. Правда, всё сено уже увезли.")
    fight_list.append("пытается получить премию Дарвина.")
    return fight_list