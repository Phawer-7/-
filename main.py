from aiogram import executor
from pymongo.errors import DuplicateKeyError
import asyncio

from simple import *
from config import chat_report, release, test
from mongoDB import usersNameExists, createColl, setDefaultNameUser, updateDefaultNameUser, deleteChatTrigger, \
    triggerChatExists
from user_triggers import deleteUserTrigger, triggerUserExists

from chatTriggers import sendTriggerList, addNewDefaultTriggerChatToColl, addNewTriggerChatToCollbyCreator, \
    addNewTriggerChatToColl, send_ready_nick, send_ready_nick
from userTriggers import sendPrivateTrigger, addPrivateTrigger, sendPersonalTriggerList


@dp.message_handler(commands=['setme', 'setMe', 'set_me'], commands_prefix='!/.')
async def setMyDefaultName(message: types.Message):
    if message.reply_to_message:
        try:
            name = message.text.split()[1]
        except IndexError:
            name = message.reply_to_message.text

        if not usersNameExists(message.from_user.id):
            setDefaultNameUser(user_id=message.from_user.id, name=name,
                               telegram_name=message.from_user.first_name,
                               username=message.from_user.username)
        else:
            updateDefaultNameUser(user_id=message.from_user.id, name=name)

        await message.answer(f'{name} установлен.')
    else:
        try:
            name = message.text.split()[1]
            if not usersNameExists(message.from_user.id):
                setDefaultNameUser(user_id=message.from_user.id, name=name,
                                   telegram_name=message.from_user.first_name,
                                   username=message.from_user.username)
            else:
                updateDefaultNameUser(user_id=message.from_user.id, name=name)
            await message.answer(f'{name} установлен.')
        except IndexError:
            await message.answer('Используйте <code>/setme [Ваше имя]</code> где вместо [Ваше имя] ставите ваш '
                                 'никнейм или имя. ', parse_mode='HTML')


@dp.message_handler(content_types=['new_chat_members'])
async def addNewChatToColl(msg: types.Message):
    if msg["new_chat_member"]["id"] == test or msg["new_chat_member"]["id"] == release:
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
        if message.chat.type == 'private':
            deleteUserTrigger(user_id=message.from_user.id, trigger_name=trigger_name)
            if not triggerUserExists(user_id=message.from_user.id, trigger_name=trigger_name):
                await message.answer(f'Триггер {trigger_name} не существовал в вашем списке.')
            else:
                await message.answer(f'Триггер {trigger_name} был удален из вашего списка.')
        else:
            deleteChatTrigger(chatId=message.chat.id, trigger_name=trigger_name)
            if not triggerChatExists(chatId=message.chat.id, trigger_name=trigger_name):
                await message.answer(f'Триггер {trigger_name} не существовал в списке.')
            else:
                await message.answer(f'Триггер {trigger_name} был удален из списка чата.')
    except IndexError:
        await message.answer('<code>/del_trigger [имя_триггера]</code>', parse_mode='HTML')


async def startTimesFunc(s, message: types.Message):
    await asyncio.sleep(s)
    await message.answer(f'Прошел {s}')


@dp.message_handler(commands=['timer'], commands_prefix='!/.')
async def startTimer(message: types.Message):
    try:
        s = message.text.split()
        asyncio.create_task(coro=startTimesFunc(int(s[1]), message))
    except IndexError:
        s = 30
        asyncio.create_task(coro=startTimesFunc(s, message))


@dp.message_handler(commands=['testKamol'], commands_prefix='!/.')
async def startTimer(message: types.Message):
    if message.from_user.id == creator:
        await message.answer('Начинаю. Каждый час в течении 5 часов.')
        for i in range(1, 6):
            y = 60*60
            asyncio.create_task(coro=startTimesFunc(y, message))


@dp.message_handler(commands=['testKamol2'], commands_prefix='!/.')
async def startTimer(message: types.Message):
    if message.from_user.id == creator:
        await message.answer('Начинаю. Каждый час в течении 1 дня')
        for i in range(1, 25):
            asyncio.create_task(coro=startTimesFunc(60*60, message))
            await message.answer(f'Прошел час. {i}')


@dp.message_handler(commands=['testKamol3'], commands_prefix='!/.')
async def startTimer(message: types.Message):
    if message.from_user.id == creator:
        await message.answer('Начинаю. Каждые 5 часов в течении 120 часов')
        for i in range(24):
            asyncio.create_task(coro=startTimesFunc(60*60*5, message))
            await message.answer(f'Прошло 5 часов. {i}')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
