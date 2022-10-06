from aiogram import Bot, Dispatcher, types
from aiogram.utils.markdown import text, code
from localization import *

from config import bot_token, chat_report

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['get_chat_id'])
async def get_id(message: types.Message):
    if not message.reply_to_message:
        await message.answer(message.chat.id)
    else:
        await message.answer(message.reply_to_message.from_user.id)


@dp.message_handler(commands=['get_my_id'])
async def get_id(message: types.Message):
    if not message.reply_to_message:
        await message.answer(message.from_user.id)
    else:
        await message.answer(message.reply_to_message.from_user.id)


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    await message.answer(f"Привет. /gir")


@dp.message_handler(commands=['dev'])
async def send_admins_username(message: types.Message):
    await message.answer('@ojfbv')


@dp.message_handler(commands=['news'])
async def get_id(message: types.Message):
    await message.answer('https://t.me/RenaissanceFlorentina')


@dp.message_handler(commands=['Гор', "гор", "gor", "Gor"], commands_prefix="!/")
async def send_nick_without_smiles(message: types.Message):
    if not message.reply_to_message:
        userName = message.from_user.first_name
        userId = message.from_user.id
    else:
        userName = message.reply_to_message.from_user.first_name
        userId = message.reply_to_message.from_user.id

    result = [i for i in userName if i in normal_char or i in caps_normal_char]
    ready_nick = "".join(result).lstrip()
    if userId == 819411604:
        await message.answer(emoji.emojize(f':joystick:{ready_nick}:musical_note:'))
    else:
        await message.answer(ready_nick)

    if not message.chat.title is None:
        await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                            f'{message.chat.title}(#{message.chat.id})')
    else:
        await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                            f'в приватном чате(#{message.chat.id})')

