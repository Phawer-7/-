from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BadRequest
import random

from localization import *

from config import bot_token, chat_report, creator, command_chat
from filters import IsAdminFilter

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)


@dp.message_handler(commands=['get_chat_id'])
async def get_chat_id(message: types.Message):
    if not message.reply_to_message:
        await message.answer(message.chat.id)
    else:
        await message.answer(message.reply_to_message.from_user.id)


@dp.message_handler(commands=['get_user_id'])
async def get_user_id(message: types.Message):
    if not message.reply_to_message:
        await message.answer(message.from_user.id)
    else:
        await message.answer(message.reply_to_message.from_user.id)


@dp.message_handler(commands=['send'])
async def sendMessageToChat(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        msgtext = " ".join(message[2:])

        await bot.send_message(chat_id=int(message[1]), text=msgtext)
        await bot.send_message(chat_report, f'Сообщение "<i>{msgtext}</i>" было отправлено в {int(message[1])}',
                               parse_mode='HTML')


@dp.message_handler(commands=['leave'])
async def leaveFromChat(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        await bot.send_message(chat_report, f'Бот использовал вышел с {int(message[1])}')
        await bot.leave_chat(chat_id=int(message[1]))


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    await message.answer(f"Привет. Я бот для турнирных чатов.")


@dp.message_handler(commands=['news'])
async def sendNewsChannel(message: types.Message):
    await message.answer('https://t.me/RenaissanceFlorentina')


@dp.message_handler(commands=['help'])
async def getHelp(message: types.Message):
    await message.answer('https://t.me/savonarola_chan')


@dp.message_handler(commands=["гур", "Гур", "Gur", "gur"], commands_prefix="/!.")
async def ban_user(message: types.Message):
    if message.from_user.id in [creator, 5197692954, 5103418171]:
        if message.reply_to_message:
            await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
            await message.reply_to_message.reply(f"Пользователь {message.reply_to_message.from_user.first_name} "
                                                 f"был забанен.")
        else:
            try:
                who = message.text.split()[1]
                await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=int(who))
                await message.answer(f"Пользователь был забанен.")
            except IndexError:
                await message.answer(f'🤨IndEr')
    else:
        await message.answer(random.choice(['🤪🤪', '🤨🤨', '😜😜']))


@dp.message_handler(commands=['опрос', 'Опрос', '0прос'], commands_prefix="!/.")
async def send_poll_gm(message: types.Message):
    if not message.chat.type == 'private':
        message_pool = message.text.split()
        del message_pool[0]
        question = " ".join(message_pool)
        poll = await bot.send_poll(chat_id=message.chat.id, question=question, is_anonymous=False,
                                   allows_multiple_answers=False, options=['Играю', "Замена", "Еще не знаю",
                                                                           "Не играю"])
        try:
            await bot.pin_chat_message(chat_id=message.chat.id, message_id=poll.message_id, disable_notification=False)
        except BadRequest:
            pass
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        await message.answer('Команда используется только в группах.')


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
