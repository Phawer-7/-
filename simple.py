from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import text, code
from localization import *

from config import bot_token

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['get_chat_id'])
async def get_id(message: types.Message):
    if not message.reply_to_message:
        await message.answer(message.chat.id)
    else:
        await message.answer(message.reply_to_message.from_user.id)


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    await message.answer(f"/гир - Получить самый обычный ник \n{code(text('/гир {цвет}'))} - Получить ник с "
                         f"определенным кругом. {code(text('/гир белый'))} даст ник с белым кругом. \nДоступные цвета: "
                         f"черный, желтый и белый")


@dp.message_handler(commands=['dev'])
async def send_admins_username(message: types.Message):
    await message.answer('@ojfbv')


@dp.message_handler(commands=['news'])
async def get_id(message: types.Message):
    await message.answer('https://t.me/RenaissanceFlorentina')


@dp.message_handler(commands=['Гор', "гор", "gor", "Gor"], commands_prefix="!/")
async def send_nick_without_smiles(message: types.Message):
    result = [i for i in message.from_user.first_name if i in normal_char or i in caps_normal_char]
    ready_nick = "".join(result).lstrip()
    await message.answer(ready_nick)