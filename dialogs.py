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

def get_mystery_dialog():
    i = random.randint(0, len(mystery_dialog_list())-1)
    return mystery_dialog_list()[i]

def get_magic_ball_dialog():
    i = random.randint(0, len(magic_ball_dialog_list())-1)
    return magic_ball_dialog_list()[i]

def fight_pos_list():
    fight_list = []
    fight_list.append("с размаху бьёт киркой")
    fight_list.append("кидает перчаткой в лицо")
    fight_list.append("делает кусь")
    fight_list.append("вызывает на дуэль и побеждает")
    fight_list.append("насмехается над")
    fight_list.append("бьёт по лицу")
    fight_list.append("выполнил идеальный гоп-стоп для")
    fight_list.append("с первой же раздачи карт собрал флеш рояль во время игры в покер с")
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

def mystery_dialog_list():
    mystery_dialog = []
    mystery_dialog.append("Что же случится дальше?")
    mystery_dialog.append("Кажется, что-то хрустнуло. Хм, интересно, что это?")
    mystery_dialog.append("Мне сейчас показалось, или погода за окном изменилась?")
    mystery_dialog.append("Вроде ничего не поменялось, но ощущение, что тут что-то не так...")
    mystery_dialog.append("Три... два... один...")
    mystery_dialog.append("Вроде выстрел был, нет?")
    mystery_dialog.append("Про глобальное потепление слышали? Так вот, вроде как сейчас оно стало наступать ещё быстрее.")
    mystery_dialog.append("Марсиане атакуют!")
    mystery_dialog.append("Код красный, код красный! Кажется, мы Советский Союз воскресили...")
    mystery_dialog.append("[Тут должна быть какая-то расисткая или феменисткая шутка, но мы выше этого]")
    mystery_dialog.append("Готовит доктор Са... bzzz... ную петлю. Вам надо сро... bzzz... та. Конец свя... bzzz...")
    mystery_dialog.append("Меня зовут Билл. И я хочу сыграть с вами в одну игру...")
    mystery_dialog.append("Somebody once told me the world is gonna roll me.")
    mystery_dialog.append("Welcome в мой dungeon, сегодня я твой master. Готовь свои three hundred bucks и я устрою тебе путешествие в deep dark fantasy.")
    mystery_dialog.append("Теперь каждый должен добавлять к своей фразе в конце \"Ня!\". Кто не справится - тот бака)) :З")
    mystery_dialog.append("Осторожней со своими желаниями, ведь они могут сбыться...")
    mystery_dialog.append("Вот есть красная нить судьбы. А у нас она почему-то коричневая и резко обрывается.")
    mystery_dialog.append("It's a trap!")
    mystery_dialog.append("Это дождь из мужиков, аллилуя!")
    mystery_dialog.append("Будьте уверены, Клементина это запомнит...")
    mystery_dialog.append("Нам сообщили, что связь с марсианской базой потеряна и там творилась какая-то чертовщина. Так что готовься к миссии, боец.")
    mystery_dialog.append("Wake the fuck up Samurai, we have a city to burn.")
    mystery_dialog.append("Помни, что тортик - это ложь! Не верь её обещаниям!")
    mystery_dialog.append("Зая, а ежедневки в геншине уже выполнены?")
    return mystery_dialog

def magic_ball_dialog_list():
    magic_ball = []
    magic_ball.append("Бесспорно")
    magic_ball.append("Предрешено")
    magic_ball.append("Никаких сомнений")
    magic_ball.append("Определённо да")
    magic_ball.append("Можешь быть уверен в этом")
    magic_ball.append("Мне кажется - да")
    magic_ball.append("Вероятнее всего")
    magic_ball.append("Хорошие перспективы")
    magic_ball.append("Знаки говорят - да")
    magic_ball.append("Да")
    magic_ball.append("Пока не ясно, попробуй снова")
    magic_ball.append("Спроси позже")
    magic_ball.append("Лучше не рассказывать")
    magic_ball.append("Сейчас нельзя предсказать")
    magic_ball.append("Сконцентрируйся и спроси опять")
    magic_ball.append("Даже не думай")
    magic_ball.append("Мне кажется - нет")
    magic_ball.append("По моим данным - нет")
    magic_ball.append("Перспективы не очень хорошие")
    magic_ball.append("Весьма сомнительно")
    magic_ball.append("Нет")
    magic_ball.append("Точно нет")
    magic_ball.append("Секретный ответ-пасхалка! А чтобы узнать ответ - спроси ещё раз")
    return magic_ball
