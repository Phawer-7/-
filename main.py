from aiogram import Bot, types, Dispatcher, executor

from localization import *

bot_token = "0000000000:AAAAAAAAAAAAAAAA"
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
admins_id = [0000000000, 0000000000, 0000000000]
chat_report = 0000000000
command_chat = 0000000000


@dp.message_handler(commands=["гур"], commands_prefix="!")
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


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    await message.reply(
        "/гир - Получить самый обычный ник \n/гир {цвет} - Получить ник с определенным кругом. \"/гир белый\" даст "
        "ник с белым кругом. Доступные цвета: черный, желтый и белый")


@dp.message_handler(commands=['get_chat_id'])
async def get_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.message_handler(commands=["Гир", "гир", "gir", "Gir"], commands_prefix="!/")
async def send_ready_nick(message: types.Message):
    result = [i for i in message.from_user.first_name if i in normal_char or i in caps_normal_char]
    ready_nick = "".join(result)

    await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                        f'{message.chat.title}(#{message.chat.id})')

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
