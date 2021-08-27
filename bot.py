import config_loader as cl
import bot_funcs as f

from datetime import datetime
import pytz
import asyncio
from aiogram import Bot, Dispatcher, executor, types

token = cl.get_token()
bot = Bot(token)
dp = Dispatcher(bot)

errorMessage = "Кажется, что-то пошло не так. Пожалуйста, сообщите администратору бота об этом случае."
userErrorMessage = "Параметры заполнены неверно. Повторите попытку."

# Запускается при первом запуске бота в ЛС.
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет, " + message.from_user.username + ".")

@dp.message_handler(commands=["test"])
async def test(message: types.Message):
    f.test()

@dp.message_handler(commands=["service_work"])
async def service_work(message: types.Message):
    if message.from_user.username == 'nuPATEXHuK':
        parameters = message.text.replace("/service_work", "").replace("@AppleBunBot", "").strip().split(" ")
        if (len(parameters) > 2):
            gold = parameters[0]
            message_text = ''
            for i, message_part in enumerate(parameters):
                if i != 0:
                    message_text += message_part + " "
            answer, chat_ids = f.service_work(gold)
        if answer != '':
            for chat_id in chat_ids:
                await bot.send_message(chat_id, message_text)
        else:
            await message.answer(errorMessage)

@dp.message_handler(commands=["fight"])
async def fight(message: types.Message):
    if (message.chat.id < 0):
        answer = userErrorMessage
        error = True
        parameter = message.text.replace("/fight", "").replace("@AppleBunBot", "").strip()
        answer = f.fight_with_player(message.from_user.id, parameter, message.chat.id)
        if (answer != ""):
            error = False
        if (error):
            await message.answer(userErrorMessage)
        else:
            await message.answer(answer)

@dp.message_handler(commands=["roll"])
async def roll(message: types.Message):
    await message.answer(f.roll(message.from_user.id, message.chat.id))

@dp.message_handler(commands=["add_free_rep"])
async def add_free_rep_for_user(message: types.Message):
    if (message.chat.id < 0):
        error = True
        parameters = message.text.replace("/add_free_rep", "").replace("@AppleBunBot", "").strip().split(" ")
        if (len(parameters) == 2):
            answer = f.restore_free_rep_for_user(message.from_user.id, parameters[0], message.chat.id, parameters[1])
            error = False
        if (error):
            await message.answer(userErrorMessage)
        else:
            await message.answer(answer)

@dp.message_handler(commands=["top_msg"])
async def top_message(message: types.Message):
    if (message.chat.id < 0):
        count = message.text.replace("/top_msg", "").replace("@AppleBunBot", "").strip().split(" ")
        answer = f.get_top_message(message.from_user.id, message.chat.id, count[0])
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["top_rep"])
async def top_rep(message: types.Message):
    if (message.chat.id < 0):
        count = message.text.replace("/top_rep", "").replace("@AppleBunBot", "").strip().split(" ")
        answer = f.get_top_rep(message.from_user.id, message.chat.id, count[0])
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["top_act"])
async def top_active(message: types.Message):
    if (message.chat.id < 0):
        count = message.text.replace("/top_act", "").replace("@AppleBunBot", "").strip().split(" ")
        answer = f.get_top_active(message.from_user.id, message.chat.id, count[0])
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["top_fight"])
async def top_fight(message: types.Message):
    if (message.chat.id < 0):
        count = message.text.replace("/top_fight", "").replace("@AppleBunBot", "").strip().split(" ")
        answer = f.get_top_fight(message.from_user.id, message.chat.id, count[0])
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["top_pirate"])
async def top_fight(message: types.Message):
    if (message.chat.id < 0):
        count = message.text.replace("/top_pirate", "").replace("@AppleBunBot", "").strip().split(" ")
        answer = f.get_top_pirate(message.from_user.id, message.chat.id, count[0])
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["top_my"])
async def top_my(message: types.Message):
    if (message.chat.id < 0):
        answer = f.get_my_top(message.from_user.id, message.from_user.username, message.chat.id)
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["gold_my"])
async def top_my(message: types.Message):
    if (message.chat.id < 0):
        answer = f.get_my_gold(message.from_user.id, message.chat.id)
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)
    else:
        await message.answer("Команда работает только в чате.")

@dp.message_handler(commands=["stat"])
async def status(message: types.Message):
    if (message.chat.id < 0):
        await message.answer(f.status_by_user(message.from_user.id, message.chat.id))
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["main_pos"])
async def main_pos(message: types.Message):
    if (message.chat.id < 0):
        await message.answer(f.get_main_pos(message.chat.id))

@dp.message_handler(commands=["main_neg"])
async def main_neg(message: types.Message):
    if (message.chat.id < 0):
        await message.answer(f.get_main_neg(message.chat.id))

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    if (message.chat.id < 0):
        await message.answer(f.get_help(message.from_user.id, message.chat.id))
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)
    else:
        await message.answer(f.get_help_PM())

@dp.message_handler(commands=["assign_title"])
async def set_title(message: types.Message):
    if (int(message.chat.id) < 0):
        answer = userErrorMessage
        error = True
        parameters = message.text.replace("/assign_title", "").replace("@AppleBunBot", "").strip().split(" ")
        if (len(parameters) >= 2):
                i = 2
                while (i < len(parameters)):
                    parameters[1] += " {}".format(parameters[i])
                    i += 1
                answer = f.set_user_title(message.from_user.id, message.chat.id, parameters)
                if (answer != ""):
                    error = False
        if (error):
            await message.answer(userErrorMessage)
        else:
            await message.answer(answer)

@dp.message_handler(commands=["random"])
async def random(message: types.Message):
    if (message.chat.id < 0):
        await message.answer(f.get_random_event(message.from_user.id, message.chat.id))
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)

@dp.message_handler(commands=["roulette"])
async def roulette(message: types.Message):
    chat_id = message.chat.id
    if (chat_id < 0):
        answer, result = f.roulette(message.from_user.id, chat_id)
        if (answer != ""):
            await message.answer(answer)
            if result:
                sti = open("stickers/boom.webp", "rb")
                await message.answer_sticker(sti)
        else:
            await message.answer(errorMessage)

@dp.message_handler(commands=["roulette_stat"])
async def roulette_stat(message: types.Message):
    if (message.chat.id < 0):
        answer = errorMessage
        try:
            roulette_current_bullets = f.chat_games[message.chat.id]
            answer = "В револьвере уже заряжены патроны в количестве {}.".format(roulette_current_bullets)
        except:
            answer = "Игра ещё не начата. Начните её командой /roulette."
        await message.answer(answer)

@dp.message_handler(commands=["stop_roulette"])
async def stop_roulette(message: types.Message):
    if (message.chat.id < 0):
        answer = errorMessage
        try:
            f.chat_games[message.chat.id]
            answer = f.stop_roulette(message.from_user.id, message.chat.id)
        except:
            answer = "Игра ещё не начата. Начните её командой /roulette."
        await message.answer(answer)

@dp.message_handler(commands=["restore"])
async def restore(message: types.Message):
    if (message.from_user.username == "nuPATEXHuK"):
        f.restore_standard_daily_params()
        await message.answer("Супер-секретная админская команда выполнена!")

@dp.message_handler(commands=["magic_ball"])
async def magic_ball(message: types.Message):
    if (message.chat.id < 0):
        answer = userErrorMessage
        error = True
        question = message.text.replace("/magic_ball", "").replace("@AppleBunBot", "").strip()
        answer = f.magic_ball(message.from_user.id, message.chat.id, question)
        if (answer != ""):
            error = False
        if error:
            await message.answer(userErrorMessage)
        else:
            await message.answer(answer)

# Грабить корованы
@dp.message_handler(commands=["rob_caravan"])
async def caravan(message: types.Message):
    answer = f.rob_caravan(message.from_user.id, message.chat.id)
    if answer != "":
        await message.answer(answer)
        await asyncio.sleep(60)
        try:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.delete_message(message.chat.id, message.message_id + 1)
        except:
            await message.answer(errorMessage)
    else:
        await message.answer(errorMessage)

@dp.message_handler(commands=["rob"])
async def rob(message: types.Message):
    if message.chat.id < 0 and message.reply_to_message is not None and message.reply_to_message.from_user.id != bot.id:
        answer = f.rob_player(message.from_user.id, message.reply_to_message.from_user.id, message.chat.id)
        if answer != "":
            await message.answer(answer)
        else:
            await message.answer(userErrorMessage)


@dp.message_handler(commands=["shop"])
async def shop(message: types.Message):
    if message.chat.id < 0:
        await message.answer("Товары магазина можно посмотреть только в личных сообщениях с ботом.")
    else:
        group = message.text.replace("/shop", "").replace("@AppleBunBot", "").strip()
        answer = f.get_shop(group)
        if answer != "":
            await message.answer(answer)
            await asyncio.sleep(3600)
            try:
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.delete_message(message.chat.id, message.message_id + 1)
            except:
                await message.answer(errorMessage)
        else:
            await message.answer(errorMessage)

@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    if message.chat.id < 0:
        item = message.text.replace("/buy", "").replace("@AppleBunBot", "").strip()
        answer = f.buy(message.from_user.id, message.chat.id, item)
        if answer != "":
            await message.answer(answer)
        else:
            await message.answer(errorMessage)
    else:
        await message.answer("Покупки можно совершать только в чате.")

@dp.message_handler(commands=["send_money"])
async def send_money(message: types.Message):
    if (int(message.chat.id) < 0):
        answer = userErrorMessage
        error = True
        parameters = message.text.replace("/send_money", "").replace("@AppleBunBot", "").strip().split(" ")
        if (len(parameters) >= 2):
                i = 2
                while (i < len(parameters)):
                    parameters[1] += " {}".format(parameters[i])
                    i += 1
                answer = f.send_money(message.from_user.id, message.chat.id, parameters)
                if (answer != ""):
                    error = False
        if (error):
            await message.answer(userErrorMessage)
        else:
            await message.answer(answer)

@dp.message_handler(commands=["save"])
async def save_money(message: types.Message):
    if message.chat.id < 0:
        money = message.text.replace("/save", "").replace("@AppleBunBot", "").strip()
        answer = f.transfer_to_bank(message.from_user.id, message.chat.id, money)
        if answer != "":
            await message.answer(answer)
        else:
            await message.answer(errorMessage)

@dp.message_handler(commands=["save_all"])
async def save_money(message: types.Message):
    if message.chat.id < 0:
        answer = f.transfer_to_bank_all(message.from_user.id, message.chat.id)
        if answer != "":
            await message.answer(answer)
        else:
            await message.answer(errorMessage)

@dp.message_handler(commands=["work"])
async def work(message: types.Message):
    answer, available = f.go_work(message.from_user.id, message.chat.id)
    if answer != "":
        if available:
            sti = open("stickers/work.webp", "rb")
            await message.answer(answer)
            await message.answer_sticker(sti)
        else:
            await message.answer(answer)
    else:
        await message.answer(errorMessage)

@dp.message_handler(commands=["bonk"])
async def bonk(message: types.Message):
    sti = open("stickers/bonk.webp", "rb")
    if (message.reply_to_message != None):
        await message.answer("{} {} делает эпичный bonk слишком horny {}!".format(f.get_user_title(message.from_user.id, message.chat.id), message.from_user.username, message.reply_to_message.from_user.username))
        await message.answer_sticker(sti)
    else:
        await message.answer("{} {} делает мульти-bonk всем, кто horny!".format(f.get_user_title(message.from_user.id, message.chat.id), message.from_user.username))
        await message.answer_sticker(sti)

@dp.message_handler(commands=["horny"])
async def horny(message: types.Message):
    if (message.from_user.username == "hikar1ya"):
        sti = open("stickers/horny.webp", "rb")
        if (message.reply_to_message != None):
            await message.answer("Госпожа {} считает, что {} слишком horny!".format(message.from_user.username, message.reply_to_message.from_user.username))
            await message.answer_sticker(sti)
        else:
            await message.answer("Госпожа {} считает, что в чате слишком много horny!".format(message.from_user.username))
            await message.answer_sticker(sti)

@dp.message_handler(commands=["block_anus"])
async def block_anus(message: types.Message):
    if (message.from_user.username == "m_boney"):
        sti = open("stickers/stethem.webp", "rb")
        if (message.reply_to_message != None):
            await message.answer("Господин {} запрещает {} творить всякие непотребства.".format(message.from_user.username, message.reply_to_message.from_user.username))
            await message.answer_sticker(sti)
        else:
            await message.answer("Господин {} запрещает всем творить здесь всякие непотребства.".format(message.from_user.username))
            await message.answer_sticker(sti)

@dp.message_handler(commands=["trap"])
async def trap(message: types.Message):
    if (message.from_user.username == "DurkNicht"):
        sti = open("stickers/trap.webp", "rb")
        await message.answer("Ахтунг! {} призван, готовьтесь принимать пикчи (и не только)!".format(message.from_user.username))
        await message.answer_sticker(sti)
    else:
        await message.answer("@DurkNicht, тут тебя зовут, людям нужны трапы!")

@dp.message_handler(commands=["booty"])
async def booty(message: types.Message):
    if (message.from_user.username == "kiyoko_koheiri"):
        sti = open("stickers/booty.tgs", "rb")
        if (message.reply_to_message != None):
            await message.answer("Госпожа {} шлёпает по жопке {}. Госпожа hikar1ya одобряет.".format(message.from_user.username, message.reply_to_message.from_user.username))
            await message.answer_sticker(sti)
        else:
            await message.answer("Госпожа {} раздаёт шлепки по жопке всему чату.".format(message.from_user.username))
            await message.answer_sticker(sti)

@dp.message_handler(commands=["super_secret_mystery_command"])
async def restore(message: types.Message):
    if (message.chat.id < 0):
        await message.answer("{} вызывает супер-секретную загадочную команду. {}".format(message.from_user.username, f.get_mystery_dialog()))

# Прослушка сообщений, сбор статистики.
@dp.message_handler(content_types=['text'])
async def message_listener(message: types.Message):
    if (message.chat.id < 0):
        if (message.from_user.id != bot.id):
            f.add_message_stat(message.chat.id, message.from_user.id, message.from_user.username, len(message.text.replace(" ", "")))
        if (message.reply_to_message != None):
            if ((message.text == "+" or message.text == "-") and message.reply_to_message.from_user.id != bot.id):
                answer = f.change_rep(message.chat.id, message.text, message.from_user.id, message.reply_to_message.from_user.id)
                if (answer != ""):
                    await message.answer(answer)
                    await asyncio.sleep(3600)
                    try:
                        await bot.delete_message(message.chat.id, message.message_id + 1)
                    except:
                        await message.answer(errorMessage)

# Функция (шедулер) для ежедневной отправки топа участников. Активна постоянно, проверятся раз в секунду.
async def scheduler(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        now = datetime.strftime(datetime.now(pytz.timezone('Europe/Moscow')), "%X")
        if (now == "00:00:00"):
            f.restore_standard_daily_params()

# Стартовая функция для запуска бота.
if __name__ == "__main__":
    # Создаём новый циклический ивент для запуска шедулера.
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(1))
    # Начало прослушки и готовности ботом принимать команды (long polling).
    executor.start_polling(dp, skip_updates=True)