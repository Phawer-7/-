from aiogram import Bot, types, Dispatcher, executor
import emoji

from localization import normal_char, caps_normal_char

bot_token = "00000000:aaaaaaaaaaaaaaaa"
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
admins_id = [00000000, 00000000]
chat_report = 00000000
command_chat = 00000000


@dp.message_handler(commands=["гур"], commands_prefix="!")
async def ban_user(message: types.Message):
    if message.from_user.id in admins_id:
        if not message.reply_to_message:
            usernamee = message.text.split()[1]

            try:
                await message.bot.kick_chat_member(chat_id=command_chat, user_id=int(usernamee))
            except ValueError:
                pass

            await message.reply_to_message.reply(f"Пользователь {usernamee} был забанен.")
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


@dp.message_handler(commands=["Гир", "гир", "gir", "Gir"])
async def send_ready_nick(message: types.Message):
    result = [i for i in message.from_user.first_name if i in normal_char or i in caps_normal_char]
    ready_nick = "".join(result)

    await bot.send_message(chat_report, f'{message.from_user.first_name} использовал {message.text} в '
                                        f'{message.chat.title}(#{message.chat.id})')

    nick = {
        "черный": emoji.emojize(f':black_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "чёрный": emoji.emojize(f':black_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "black": emoji.emojize(f':black_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "желтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "yellow": emoji.emojize(f':yellow_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "жёлтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|{ready_nick}🌅'),
        'мизан': emoji.emojize(f'𝖑𝖎𝖗||{ready_nick}'),
        'мизантроп': emoji.emojize(f':black_circle:𝖑𝖎𝖗||{ready_nick}'),
        "белый": emoji.emojize(f':white_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "white": emoji.emojize(f':white_circle:🎻ʀᴇ|{ready_nick}🌅'),
        "ktm": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{ready_nick}🐈'),
        "katsu": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{ready_nick}🐈'),
        "катсу": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{ready_nick}🐈'),
        "нюдсы": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{ready_nick}🐈'),
    }

    malik = {
        "белый": emoji.emojize(f':white_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
        "white": emoji.emojize(f':white_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
        "черный": emoji.emojize(f':black_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
        "black": emoji.emojize(f':black_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
        "чёрный": emoji.emojize(f':black_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
        "желтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
        "жёлтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'),
    }

    try:
        color = message.text.split()[1]

        if message.from_user.id == 819411604:
            await message.answer(malik[color])
        else:
            await message.answer(nick[color])
    except IndexError:
        if message.from_user.id == 819411604:
            await message.answer(emoji.emojize(f'🎻ʀᴇ|:joystick:{ready_nick}:musical_note:🌅'))
        else:
            await message.answer(f'🎻ʀᴇ|{ready_nick}🌅')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
