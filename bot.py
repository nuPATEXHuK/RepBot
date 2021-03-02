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


# Запускается при первом запуске бота в ЛС.
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет, " + message.from_user.username + ".")

@dp.message_handler(commands=["stat"])
async def status(message: types.Message):
    await message.answer(f.status_by_user(message.from_user.id, message.chat.id))
    await asyncio.sleep(60)
    # Опасное место, надо повесить сюда try
    await bot.delete_message(message.chat.id, message.message_id + 1)

@dp.message_handler(content_types=['text'])
async def rep_change(message: types.Message):
    if (message.chat.id < 0):
        if (message.from_user.id != bot.id):
            f.add_message_stat(message.chat.id, message.from_user.id, message.from_user.username, len(message.text.replace(" ", "")))
        if (message.reply_to_message != None):
            if (message.text == "+" or message.text == "-"):
                answer = f.change_rep(message.chat.id, message.text, message.from_user.id, message.reply_to_message.from_user.id)
                if (answer != ""):
                    await message.answer(answer)
                    await asyncio.sleep(30)
                    # Опасное место, надо повесить сюда try
                    await bot.delete_message(message.chat.id, message.message_id + 1)

# Функция (шедулер) для ежедневной отправки топа участников. Активна постоянно, проверятся раз в секунду.
async def scheduler(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        now = datetime.strftime(datetime.now(pytz.timezone('Europe/Moscow')), "%X")
        #if (now == "00:00:00"):
        #    activeConferences = f.get_all_conferences()
        #    for Conference in activeConferences:
        #        await bot.send_message(activeReleases[Conference], f.get_top_rep_list(), disable_notification=True)

# Стартовая функция для запуска бота.
if __name__ == "__main__":
    # Создаём новый циклический ивент для запуска шедулера.
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler(1))
    # Начало прослушки и готовности ботом принимать команды (long polling).
    executor.start_polling(dp, skip_updates=True)