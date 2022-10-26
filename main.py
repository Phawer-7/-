from aiogram import executor
from pymongo.errors import DuplicateKeyError

from simple import *
from config import chat_report, release, test
from mongoDB import usersNameExists, getTriggerList, createColl, createNewTrigger, setDefaultTriggerChat, \
    setDefaultNameUser, updateDefaultNameUser, defaultSmilesAreadyExists, updateDefaultSmilesChat
from manipulationWithName import returnWithoutSmiles
from user_triggers import createUserColl, userExists, createNewUserTrigger, updateUserTrigger, TriggerAlreadyExists, \
    getPersonalTriggerList


@dp.message_handler(commands=["Гир", "гир", "gir", "Gir"], commands_prefix="!/.")
async def send_ready_nick(message: types.Message):
    if message.reply_to_message:
        membersName = message.reply_to_message.from_user.first_name
        membersId = message.reply_to_message.from_user.id
    else:
        membersName = message.from_user.first_name
        membersId = message.from_user.id

    if not usersNameExists(membersId):
        ready_nick = returnWithoutSmiles(membersName)
        if ready_nick == 0:
            result = [i for i in membersName if i in normal_char or i in caps_normal_char]
            ready_nick = "".join(result).lstrip()
            if len(ready_nick) == 0:
                ready_nick = membersName
    else:
        ready_nick = usersNameExists(membersId)

    try:
        ready_name = send_name(chat_id=message.chat.id, name=ready_nick, color=message.text.split()[1])
        await message.answer(ready_name)
    except IndexError:
        ooo = send_name(chat_id=message.chat.id, name=ready_nick, default=True, color=0)
        if not ooo == 'Такого триггера не существует':
            await message.answer(ooo)
        else:
            await message.answer(f'🎻ʀᴇ|{ready_nick}🌅')

    if not message.chat.title is None:
        await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                            f'{message.chat.title}(#{message.chat.id})')
    else:
        await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                            f'в приватном чате(#{message.chat.id})')


@dp.message_handler(commands=['aki', 'Aki'], is_admin=True, commands_prefix='!/.')
async def addNewChatToColl(msg: types.Message):
    if not msg.chat.type == 'private':
        try:
            if not msg.reply_to_message:
                message = msg.text.split()
                trigger_name = message[1]
                ind = msg.text.find(message[2])
                value = msg.text[ind:]

                index = value.find('NAME')
                if not index == -1:
                    res = [value[:index], value[index + 4:]]
                else:
                    res = value
            else:
                trigger_name = msg.text.split()[1]
                value = msg.reply_to_message.text

                index = value.find('NAME')
                if not index == -1:
                    res = [value[:index], value[index + 4:]]
                else:
                    res = value

            createNewTrigger(collect_name=msg.chat.id, trigger_name=trigger_name, trigger_value=res)
            await msg.answer(f'Триггер <code>{trigger_name}</code> добавлен в список. Используйте /list_triggers чтобы '
                             f'получить список.', parse_mode='HTML')
        except IndexError:
            await msg.answer("Недостаточно аргументов. \nПример команды: `!aki [trigger] [sample]`\n"
                             "[Подробнее о sample(шаблонах) читайте тут](https://t.me/savonarola_chan/2)",
                             parse_mode='Markdown', disable_web_page_preview=True)
    else:
        await msg.answer('Используйте команду в чате.')


@dp.message_handler(commands=['aki'], commands_prefix='!/.')
async def addNewChatToColl(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        trigger_name = message[1]
        ind = msg.text.find(message[2])
        value = msg.text[ind:]

        index = value.find('NAME')
        if not index == -1:
            res = [value[:index], value[index + 4:]]
        else:
            res = value

        createNewTrigger(collect_name=msg.chat.id, trigger_name=trigger_name, trigger_value=res)
        await msg.answer(f'Триггер <code>{trigger_name}</code> добавлен в список. Используйте /list_triggers чтобы '
                         f'получить список.', parse_mode='HTML')


@dp.message_handler(commands=['default'], is_admin=True, commands_prefix='!/.')
async def addNewChatToColl(msg: types.Message):
    try:
        if msg.reply_to_message:
            value = msg.reply_to_message.text[9:]
        else:
            value = msg.text[9:]

        index = value.find('NAME')
        if not index == -1:
            res = [value[:index], value[index + 4:]]
        else:
            res = value

        if not defaultSmilesAreadyExists(msg.chat.id):
            setDefaultTriggerChat(chat_id=msg.chat.id, chatName=msg.chat.title, trigger_value=res)
            await msg.answer(f'Установлены новые смайлы по умолчанию.🔥\nИспользуйте /list_triggers чтобы получить '
                             f'список всех триггеров этого чата.', parse_mode='HTML')
        else:
            updateDefaultSmilesChat(chat_id=msg.chat.id, default_trigger=res)
            await msg.answer(f'Обновлены смайлы по умолчанию.🔥\nИспользуйте /list_triggers чтобы получить '
                             f'список всех триггеров этого чата.', parse_mode='HTML')
    except IndexError:
        await msg.answer('Недостаточно аргументов. ')


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


@dp.message_handler(commands=['ger'], commands_prefix='!/.#')
async def sendPrivateTrigger(message: types.Message):
    if not userExists(message.from_user.id):
        createUserColl(user_id=message.from_user.id, name=message.from_user.first_name,
                       username=message.from_user.username)

    if message.reply_to_message:
        membersName = message.reply_to_message.from_user.first_name
        membersId = message.reply_to_message.from_user.id
    else:
        membersName = message.from_user.first_name
        membersId = message.from_user.id

    if not usersNameExists(membersId):
        ready_nick = returnWithoutSmiles(membersName)
        if ready_nick == 0:
            result = [i for i in membersName if i in normal_char or i in caps_normal_char]
            ready_nick = "".join(result).lstrip()
            if len(ready_nick) == 0:
                ready_nick = membersName
    else:
        ready_nick = usersNameExists(membersId)

    try:
        ready_name = personal_sendName(user_id=message.from_user.id, name=ready_nick,
                                       trigger_name=message.text.split()[1])
        await message.answer(ready_name)
    except IndexError:
        await message.answer(f'<code>/ger [триггер]</code>.', parse_mode='HTML')


@dp.message_handler(commands=['private'], commands_prefix='!/.#')
async def addPrivateTrigger(message: types.Message):
    if message.chat.type == 'private':
        if not userExists(message.from_user.id):
            createUserColl(user_id=message.from_user.id, name=message.from_user.first_name,
                           username=message.from_user.username)
            await message.answer('Добавил в базу...')

        try:
            trigger_settings = message.text.split()
            trigger_name = trigger_settings[1]
            ind = message.text.find(trigger_settings[2])
            value = message.text[ind:]
            index = value.find('NAME')
            if not index == -1:
                res = [value[:index], value[index + 4:]]
            else:
                res = value

            if not TriggerAlreadyExists(user_id=message.from_user.id, name=trigger_name):
                createNewUserTrigger(user_id=message.from_user.id, trigger_name=trigger_name,
                                     trigger_value=res)
                await message.answer(f'{trigger_name} успешно добавлен.')
            else:
                updateUserTrigger(user_id=message.from_user.id, trigger_name=trigger_name, trigger_value=res)
                await message.answer(f'{trigger_name} успешно обновлен.')
        except IndexError:
            await message.answer(f'<code>/private триггер шаблон</code>.', parse_mode='HTML')
    else:
        await message.answer('Команда работает только в личных сообщениях.')


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


@dp.message_handler(commands=['list', 'triggers', 'chat_triggers', 'list_triggers'], commands_prefix='/!.#')
async def sendTriggerList(message: types.Message):
    if not message.chat.type == 'private':
        await message.answer(f'{getTriggerList(message.chat.id)}')
    else:
        await message.answer('Команда используется в чате.')


@dp.message_handler(commands=['mylist', 'mytriggers', 'my_triggers', 'my_list_triggers'], commands_prefix='/!.#')
async def sendPersonalTriggerList(message: types.Message):
    if getPersonalTriggerList(message.from_user.id) == 'Список личных триггеров:\n':
        await message.answer('У вас пока нет личных триггеров.')
    else:
        await message.answer(f'{getPersonalTriggerList(message.from_user.id)}')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
