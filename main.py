from aiogram import executor
from pymongo.errors import DuplicateKeyError
from aiogram.utils.exceptions import BadRequest

from simple import *
from config import chat_report, release, test, debug_commands
from mongoDB import usersNameExists, getTriggerList, createColl, createNewTrigger, setDefaultTriggerChat, \
    setDefaultNameUser, updateDefaultNameUser
from manipulationWithName import returnWithoutSmiles

DEBUG = True


@dp.message_handler(commands=[debug_commands['get_trigger'][DEBUG], "Гир", "гир", "gir", "Gir"], commands_prefix="!/.")
async def send_ready_nick(message: types.Message):
    if message.reply_to_message:
        membersName = message.reply_to_message.from_user.first_name
        membersId = message.reply_to_message.from_user.id
    else:
        membersName = message.from_user.first_name
        membersId = message.from_user.id

    if not usersNameExists(membersId):
        result = returnWithoutSmiles(membersName)
        print(result)
        ready_nick = result
        if result == 0:
            result = [i for i in membersName if i in normal_char or i in caps_normal_char]
            ready_nick = "".join(result).lstrip()
        print(ready_nick)
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


@dp.message_handler(commands=['aki', debug_commands['add_new_trigger'][DEBUG]], is_admin=True, commands_prefix='!/.')
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

        setDefaultTriggerChat(collect_name=msg.chat.id, chatName=msg.chat.title, trigger_value=res)
        await msg.answer(f'Установлены новые смайлы по умолчанию.🔥\n Используйте /list_triggers чтобы получить '
                         f'список всех триггеров этого чата.', parse_mode='HTML')
    except IndexError:
        await msg.answer('Недостаточно аргументов. ')


@dp.message_handler(commands=['setme', 'setMe', 'set_me', debug_commands['add_user_name'][DEBUG]], commands_prefix='!/.')
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


@dp.message_handler(commands=['опрос', 'Опрос', '0прос'], commands_prefix="!/.")
async def send_poll_gm(message: types.Message):
    if not message.chat.type == 'private':
        message_pool = message.text.split()
        del message_pool[0]
        question = " ".join(message_pool)
        poll = await bot.send_poll(chat_id=message.chat.id, question=question, is_anonymous=False,
                                   allows_multiple_answers=False, options=['Играю', "Замена", "Еще не знаю", "Не играю"])
        try:
            await bot.pin_chat_message(chat_id=message.chat.id, message_id=poll.message_id, disable_notification=False)
        except BadRequest:
            pass
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        await message.answer('Команда используется только в группах.')


@dp.message_handler(commands=['import'])
async def importTriggers(msg: types.Message):
    try:
        chat = msg.text.split()[1]

        if chat == '-1001674111955':
            await msg.answer(f'Триггеры с чата Renaissance были скопированы.')
        elif chat == 'recommended_list':
            await msg.answer(f'Рекомендованные триггеры были скопированы.')
        else:
            await msg.answer(f'Триггеры с чата {chat} были скопированы.')
    except IndexError:
        await msg.answer(f"Недостаточно аргументов было передано. Пример: <code>/import -1001674111955</code>",
                         parse_mode='HTML')


@dp.message_handler(commands=['list', 'triggers', 'chat_triggers', 'list_triggers'], commands_prefix='/!.#')
async def sendTriggerList(message: types.Message):
    if not message.chat.type == 'private':
        await message.answer(f'{getTriggerList(message.chat.id)}')
    else:
        await message.answer('Команда используется в чате.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
