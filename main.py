from aiogram import executor
from pymongo.errors import DuplicateKeyError

import config
from manipulationWithName import returnWithoutSmiles
from simple import *
from config import chat_report, release, test
from mongoDB import usersNameExists, createColl, setDefaultNameUser, updateDefaultNameUser, deleteChatTrigger, \
    triggerChatExists
from user_triggersDB import deleteUserTrigger, triggerUserExists
from tools import textWithoutCommand

import chatTriggers
import userTriggers
import gamepoll.gamepoll
import gamepoll.addingList


@dp.message_handler(commands=['setme', 'setMe', 'set_me'], commands_prefix='!/.')
async def setMyDefaultName(message: types.Message):
    msg = message.from_user
    if message.reply_to_message and message.from_user.id == config.creator:
        msg = message.reply_to_message.from_user

    name = textWithoutCommand(message.text)
    if name is None:
        await message.answer('Используйте <code>/setme [Ваше имя]</code> где вместо [Ваше имя] ставите ваш '
                             'никнейм или имя. ', parse_mode='HTML')
        return

    if not usersNameExists(msg.id):
        setDefaultNameUser(user_id=msg.id, name=name,
                           telegram_name=msg.first_name,
                           username=msg.username)
    else:
        updateDefaultNameUser(user_id=msg.id, name=name)
    await message.answer(f'{name} установлен.')


@dp.message_handler(commands=['setname', 'set_name'], commands_prefix='!/.')
async def setMyDefaultNameByCoping(message: types.Message):
    if message.reply_to_message and message.from_user.id == config.creator:
        name = message.reply_to_message.from_user.first_name
        msg = message.reply_to_message.from_user
    else:
        name = message.from_user.first_name
        msg = message.from_user

    if not usersNameExists(msg.id):
        setDefaultNameUser(user_id=msg.id, name=name,
                           telegram_name=msg.first_name,
                           username=msg.username)
    else:
        updateDefaultNameUser(user_id=msg.id, name=name)

    await message.answer(f'{name} установлен.')


@dp.message_handler(commands=['check'], commands_prefix='!/.')
async def checkHowItWorks(message: types.Message):
    nickname = textWithoutCommand(message.text)
    if not nickname is None:
        ready_nick = returnWithoutSmiles(nickname)
        if ready_nick == 0:
            result = [i for i in nickname if i in normal_char or i in caps_normal_char]
            ready_nick = "".join(result).lstrip()
            if len(ready_nick) == 0:
                ready_nick = nickname
        await message.answer(f"🎻ʀᴇ| {ready_nick} 🌅")


@dp.message_handler(content_types=['new_chat_members'])
async def addNewChatToColl(msg: types.Message):
    if msg["new_chat_member"]["id"] == test or msg["new_chat_member"]["id"] == release:
        buttons = [
            types.InlineKeyboardButton(text="Канал бота", url="https://t.me/savonarola_chan"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(buttons[0])
        await msg.answer('Привет. Я бот для турнирных чатов. Документация еще не готова но осталось совсем немного. '
                         'Но уже есть телеграм канал где объясняются некоторые фишки бота.', reply_markup=keyboard)
        try:
            createColl(chat_id=msg.chat.id, name=msg.chat.title)

            m = await bot.send_message(chat_id=chat_report, text=f'NEW\ngroup: {msg.chat.title}, id: {msg.chat.id}')
            await bot.pin_chat_message(chat_id=chat_report, message_id=m['message_id'])
        except DuplicateKeyError:
            pass
    elif msg["new_chat_member"]["id"] == creator:
        await msg.answer(f'Привет, {msg.from_user.first_name}!⚡️')


@dp.message_handler(commands=['del', 'delete', 'del_trigger'], is_admin=True, commands_prefix='!/.')
async def deleteTrigger(message: types.Message):
    try:
        trigger_name = message.text.split()[1]
        if not message.chat.type == 'private':
            deleteChatTrigger(chatId=message.chat.id, trigger_name=trigger_name)
            if not triggerChatExists(chatId=message.chat.id, trigger_name=trigger_name):
                await message.answer(f'Триггер {trigger_name} не существовал в списке.')
            else:
                await message.answer(f'Триггер {trigger_name} был удален из списка чата.')
    except IndexError:
        await message.answer('<code>/del_trigger [имя_триггера]</code>', parse_mode='HTML')


@dp.message_handler(commands=['del', 'delete', 'del_trigger'], commands_prefix='!/.')
async def deleteTrigger2(message: types.Message):
    try:
        trigger_name = message.text.split()[1]
        if message.chat.type == 'private':
            deleteUserTrigger(user_id=message.from_user.id, trigger_name=trigger_name)
            if not triggerUserExists(user_id=message.from_user.id, trigger_name=trigger_name):
                await message.answer(f'Триггер {trigger_name} не существовал в вашем списке.')
            else:
                await message.answer(f'Триггер {trigger_name} был удален из вашего списка.')
    except IndexError:
        await message.answer('<code>/del_trigger [имя_триггера]</code>', parse_mode='HTML')


@dp.message_handler(content_types=["text"])
async def PinMafiaList(message: types.Message):
    if message.chat.id == config.command_chat or message.chat.id == -1001829614132:
        if message.text.startswith('Запомни своих союзников'):
            await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)
        elif message.text.startswith("Добро пожаловать во"):
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    elif message.chat.id == -1001591495273:
        if message.text.startswith('Запомни своих союзников'):
            await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
