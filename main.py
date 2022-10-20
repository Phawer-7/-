from aiogram import executor

from simple import *
from config import admins_id, chat_report, command_chat, r, t, creator
from db import SQLighter
from mongoDB import *
from pymongo.errors import DuplicateKeyError

db = SQLighter("users.db")


@dp.message_handler(commands=["гур", "Гур", "Gur", "gur"], commands_prefix="/!")
async def ban_user(message: types.Message):
    if message.from_user.id in admins_id:
        if not message.reply_to_message:
            userId = message.text.split()[1]

            try:
                await message.bot.kick_chat_member(chat_id=command_chat, user_id=int(userId))
            except ValueError:
                pass

            await message.reply_to_message.reply(f"Пользователь {userId} был забанен.")
            return

        await message.bot.kick_chat_member(chat_id=command_chat, user_id=message.reply_to_message.from_user.id)

        await message.reply_to_message.reply(f"Пользователь {message.reply_to_message.from_user.first_name} был "
                                             f"забанен.")
    else:
        await message.answer("Ты чо за нн?")


@dp.message_handler(commands=['опрос', 'Опрос', '0прос'], commands_prefix="!/. ")
async def send_pool(message: types.Message):
    message_pool = message.text.split()
    del message_pool[0]
    question = " ".join(message_pool)
    await message.answer(f'{message.from_user.first_name} запустил опрос {question}')
    poll = await bot.send_poll(chat_id=message.chat.id, question=question, is_anonymous=False,
                               allows_multiple_answers=False, options=['Играю', "Замена", "Еще не знаю", "Не играю"])
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=poll.message_id, disable_notification=False)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler(commands=["Гир", "гир", "gir", "Gir"], commands_prefix="!/")
async def send_ready_nick(message: types.Message):
    if not message.reply_to_message:
        result = [i for i in message.from_user.first_name if i in normal_char or i in caps_normal_char]
    else:
        result = [i for i in message.reply_to_message.from_user.first_name if i in normal_char or i in caps_normal_char]
    ready_nick = "".join(result).lstrip()

    if not message.chat.title is None:
        await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                            f'{message.chat.title}(#{message.chat.id})')
    else:
        await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                            f'в приватном чате(#{message.chat.id})')
    try:
        ready_name = send_name(chat_id=message.chat.id, name=ready_nick, color=message.text.split()[1], user_id=message.from_user.id)
        await message.answer(ready_name)

    except IndexError:
        if message.from_user.id == 819411604:  # exception for @minusoo
            await message.answer(emoji.emojize(f'🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'))
        else:
            await message.answer(f'🎻ʀᴇ|{ready_nick}🌅')


@dp.message_handler(content_types=['new_chat_members'])
async def addNewChatToColl(msg: types.Message):
    if msg["new_chat_member"]["id"] == t or msg["new_chat_member"]["id"] == r:
        try:
            createColl(chat_id=msg.chat.id, name=msg.chat.title)
        except DuplicateKeyError:
            pass


@dp.message_handler(commands=['addToDB'])
async def addNewChatToColl(msg: types.Message):
    createColl(chat_id=msg.chat.id, name=msg.chat.title)


@dp.message_handler(commands=['send'])
async def addNewChatToColl(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        msgtext = " ".join(message[2:])

        await bot.send_message(chat_id=int(message[1]), text=msgtext)
        await bot.send_message(chat_report, f'Сообщение "<i>{msgtext}</i>" было отправлено в {int(message[1])}',
                               parse_mode='HTML')


@dp.message_handler(commands=['leave'])
async def addNewChatToColl(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        await bot.send_message(chat_report, f'Бот использовал вышел с {int(message[1])}')
        await bot.leave_chat(chat_id=int(message[1]))


@dp.message_handler(commands=['import'])
async def addNewChatToColl(msg: types.Message):
    pass


@dp.message_handler(commands=['list'], commands_prefix='/!.#')
async def sendTriggerList(message: types.Message):
    if not message.chat.type == 'private':
        await message.answer(f'{getTriggerList(message.chat.id)}')


@dp.message_handler(commands=['aki'])
async def addNewChatToColl(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        value = [message[2:][0], message[2:][2]]
        print(value)
        createNewTrigger(collect_name=msg.chat.id, trigger_name=message[1], trigger_value=value)
        await msg.answer(f'Триггер <code>{message[1]}</code> добавлен в список. Используйте /list чтобы '
                         f'получить список.', parse_mode='HTML')


@dp.message_handler(commands=['default'])
async def addNewChatToColl(msg: types.Message):
    if msg.from_user.id == creator:
        message = msg.text.split()
        value = [message[2:][0], message[2:][2]]
        setDefaultTriggerChat(collect_name=msg.chat.id, trigger_name=message[1], trigger_value=value)
        await msg.answer(f'Триггер <code>{message[1]}</code> установлен как триггер по умолчанию. При вызове /gir '
                         f'без аргументов будет отправляться этот триггер.', parse_mode='HTML')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
