import config_loader as cl
import bot_funcs as f

import logging
from datetime import datetime
import pytz
import asyncio
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

token = cl.get_token()
bot = Bot(token)
dp = Dispatcher(bot)

errorMessage = "Кажется, что-то пошло не так. Пожалуйста, сообщите администратору бота об этом случае."
userErrorMessage = "Параметры заполнены неверно. Повторите попытку."

# Запускается при первом запуске бота в ЛС.
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет, " + message.from_user.username + ".")

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

@dp.message_handler(commands=["roulette"])
async def roulette(message: types.Message):
    if (message.chat.id < 0):
        answer = userErrorMessage
        error = True
        parameter = message.text.replace("/roulette", "").replace("@AppleBunBot", "").strip()
        answer = f.roulette(message.from_user.id, message.chat.id, parameter)
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
            chat_ids = f.get_all_chat_ids()
            if (len(chat_ids) > 0):
                for chat_id in f.get_all_chat_ids():
                    await bot.send_message(chat_id, "Дамы и господа, подводим итоги дня!")
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "В эфире передача 💥 \"Русская рулетка\" 💥!\nИтак, давайте же узнаем, кто у нас на сегодня сыграл в ящик.")
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "3 - ищем улики на месте преступления 🔍")
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "2 - проверяем подворотни 👀")
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "1 - обзванием морги ☎️")
                    await asyncio.sleep(1)
                    dead_list = f.get_all_dead(chat_id)
                    if (len(dead_list) > 0):
                        dead_report = ""
                        for dead in dead_list:
                            dead_report += dead + ".\nПричина смерти: " + f.dialogs.get_cause_of_death() + "\n"
                            dead_report += "\n Помянем павших."
                        await bot.send_message(chat_id, "А вот и список мертвецов на сегодня, которые бросили вызов и проиграли:\n{}".format(dead_report))
                    else:
                        await bot.send_message(chat_id, "Вот это да! Ни единого трупа не нашлось. Что это? Удача? Или же страх перед опасной игрой? 😏")
                    await asyncio.sleep(3)
                    await bot.send_message(chat_id, "Но это ещё не всё. Давайте посмотрим, кто у нас сегодня {}, а кто {}".format(f.dialogs.get_fight_top(), f.dialogs.get_fight_loser()))
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "3 - считаем циферки с уроном 🧮")
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "2 - заглядываем на главную арену чата ⚔️🛡")
                    await asyncio.sleep(1)
                    await bot.send_message(chat_id, "1 - строим на глаз график побед и поражений 📈📉")
                    await asyncio.sleep(1)
                    fight_top = f.get_fight_top(chat_id)
                    fight_loser = f.get_fight_loser(chat_id)
                    await bot.send_message(chat_id, "Лучший боец:\n{}\n\nХудший боец:\n{}".format(fight_top, fight_loser))
            f.restore_standard_daily_params()

# Стартовая функция для запуска бота.
if __name__ == "__main__":
    # Создаём новый циклический ивент для запуска шедулера.
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(1))
    # Начало прослушки и готовности ботом принимать команды (long polling).
    executor.start_polling(dp, skip_updates=True)