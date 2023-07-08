from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types.input_file import InputFile
from aiogram.types.message import ContentType

from config import TOKEN, ADMINS_ID
from db import database, connect_to_db

#Модель бота и клас диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
db = database()

@dp.message_handler(commands=["start"])
async def start_command(message : types.Message):
    db_ansver = await db.insert_user(message.from_user.id)
    if db_ansver["status"]:
        await bot.send_message(message.from_user.id, """Привет!
            
<b>Главное меню</b>""")
    else: await bot.send_message("Что-то пошло не так")
    await message.delete()

@dp.message_handler(commands=["admin"])
async def start_command(message : types.Message):
    for id in ADMINS_ID:
        if str(message.chat.id) == id:
            await bot.send_message(message.from_user.id, "Привет админ!")
            await message.delete()
            break

#Функция которая запускается со стартом бота
async def on_startup(_):
    await db.connect_to_db()
    print('bot online')
#Пулинг бота
executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #Пуллинг бота

#Вывод уведомления про отключение бота
print("Bot offline")