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

@dp.message_handler(commands=["stat"])
async def status(message: types.Message):
    await message.answer(f.status_by_user(message.from_user.id, message.chat.id))
    await asyncio.sleep(60)
    try:
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.message_id + 1)
    except:
        await message.answer(errorMessage)

@dp.message_handler(commands=["assign_user_title"])
async def set_title(message: types.Message):
    if (int(message.chat.id) < 0):
        answer = userErrorMessage
        error = True
        parameters = message.text.replace("/assign_user_title", '').replace("@AppleBunBot", "").strip().split(" ")
        if (len(parameters) >= 2):
                i = 2
                while (i < len(parameters)):
                    parameters[1] += " {}".format(parameters[i])
                    i += 1
                answer = f.set_user_title(message.from_user.id, message.chat.id, parameters)
                if (answer != ""):
                    error = False
        if (error):
            try:
                await bot.delete_message(message.chat.id, message.message_id)
                await bot.delete_message(message.chat.id, message.message_id + 1)
            except:
                await message.answer(errorMessage)
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
                    await asyncio.sleep(30)
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
            f.restore_free_rep()
            #activeConferences = f.get_all_conferences()
            #for Conference in activeConferences:
            #    await bot.send_message(activeReleases[Conference], f.get_top_rep_list(), disable_notification=True)

# Стартовая функция для запуска бота.
if __name__ == "__main__":
    # Создаём новый циклический ивент для запуска шедулера.
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(1))
    # Начало прослушки и готовности ботом принимать команды (long polling).
    executor.start_polling(dp, skip_updates=True)