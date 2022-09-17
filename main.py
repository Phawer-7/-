from aiogram import executor
from aiogram.types import ParseMode

from simple import *
from config import admins_id, chat_report, command_chat
from db import SQLighter
from players_poll import trueMafia

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


@dp.message_handler(commands=['list'], commands_prefix="!/")
async def send_list_of_triggers(message: types.Message):
    monotext = text(code("/gir trigger"))
    await message.answer(f'{monotext}\nСписок triggers:\n\n{send_name(return_dict=True)}', parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['опрос', 'Опрос', '0прос'], commands_prefix="!/. ")
async def send_pool(message: types.Message):
    message_pool = message.text.split()
    del message_pool[0]
    question = " ".join(message_pool)
    await message.answer(f'{message.from_user.first_name} запустил опрос {question}')
    await bot.send_poll(chat_id=message.chat.id, question=question, is_anonymous=False,
                        allows_multiple_answers=False, options=['Играю', "Замена", "Еще не знаю", "Не играю"])
    await bot.pin_chat_message(chat_id=message.chat.id, message_id=(message.message_id + 2), disable_notification=False)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.poll_answer_handler()
async def poll_answer(poll_answer: types.PollAnswer):
    if poll_answer['option_ids'][0] == 0:
        db.add_user(username=poll_answer['user']['username'], id=poll_answer['user']['id'])

        if len(db.get_users()) == 10:
            bot.send_message(admins_id[0], 'Собрали достаточно людей')


@dp.message_handler(commands=['список_Трушка'], commands_prefix="!/")
async def send_list_of_players(message: types.Message):
    try:
        username = message.text.split()[1]
        if len(db.get_users()) == 10:
            users = trueMafia(db.get_users(), captain=username)
        elif len(db.get_users()) > 10:
            users = trueMafia(db.get_users()[:9], captain=username)
        await bot.send_message(message.chat.id, users)
    except IndexError:
        if len(db.get_users()) == 10:
            users = trueMafia(db.get_users())
        elif len(db.get_users()) > 10:
            users = trueMafia(db.get_users()[:9])
        await bot.send_message(message.chat.id, users)


@dp.message_handler(commands=['clear_db'], content_types='!/')
async def clear(message: types.Message):
    pass


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
        ready_name = send_name(name=ready_nick, color=message.text.split()[1], user_id=message.from_user.id)
        await message.answer(ready_name)

    except IndexError:
        if message.from_user.id == 819411604:  # exception for @minusoo
            await message.answer(emoji.emojize(f'🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'))
        else:
            await message.answer(f'🎻ʀᴇ|{ready_nick}🌅')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
