from aiogram import types
from aiogram.utils.exceptions import MessageToEditNotFound

from simple import bot, dp
from gamepoll.regDB import addUsername, addMessageId, getId, getUsers, removeUsername, updateCaptain, getCaptain, \
    del_users_and_messageId, updateMessageId
from gamepoll.arrayfunc import MafiaArray


buttonsTrue = [
    types.InlineKeyboardButton(text="Играю", callback_data='1t'),
    types.InlineKeyboardButton(text="Появились дела, не играю", callback_data='0t')
]
keyboardTrue = types.InlineKeyboardMarkup(row_width=1)
keyboardTrue.add(buttonsTrue[0])
keyboardTrue.add(buttonsTrue[1])

buttonsBaku = [
    types.InlineKeyboardButton(text="Играю", callback_data='1b'),
    types.InlineKeyboardButton(text="Появились дела, не играю", callback_data='0b')
]
keyboardBaku = types.InlineKeyboardMarkup(row_width=1)
keyboardBaku.add(buttonsBaku[0])
keyboardBaku.add(buttonsBaku[1])

values = ['baku', 'Baku', 'Баку', 'баку']


@dp.message_handler(commands=['regist', 'registration', 'start_reg'], commands_prefix="!/.")
async def start_registration(message: types.Message):
    try:
        captain = message.text.split()[-1]
        game_bot = message.text.split()[1]

        if game_bot in values:
            isTrue = False
            kb = buttonsBaku
        else:
            isTrue = True
            kb = buttonsTrue

        if captain == 'me':
            if message.from_user.username is not None:
                captain = f"@{message.from_user.username}"
            else:
                captain = f'{message.from_user.first_name}'
    except IndexError:
        captain = '@captain'
        isTrue = True
        kb = buttonsTrue

    updateCaptain(username=captain, chatID=message.chat.id, true=isTrue)

    if getId(chatId=message.chat.id, true=isTrue) == 0:
        if isTrue:
            msg = await message.answer(MafiaArray(usernames=[], captain=captain, team=message.chat.id, isTrue=isTrue),
                                       reply_markup=keyboardTrue)
        else:
            msg = await message.answer(MafiaArray(usernames=[], captain=captain, team=message.chat.id, isTrue=isTrue),
                                       reply_markup=keyboardBaku)
        updateMessageId(message_id=msg['message_id'], chatID=message.chat.id, true=isTrue)
    elif getId(message.chat.id, true=isTrue) == 'do not exists':
        if isTrue:
            msg = await message.answer(MafiaArray(usernames=[], captain=captain, team=message.chat.id, isTrue=isTrue),
                                       reply_markup=keyboardTrue)
        else:
            msg = await message.answer(MafiaArray(usernames=[], captain=captain, team=message.chat.id, isTrue=isTrue),
                                       reply_markup=keyboardBaku)
        addMessageId(message_id=msg['message_id'], chatName=message.chat.title, chatId=message.chat.id, captain=captain,
                     true=isTrue)
    else:
        await message.answer('Сначала останови предыдущую регистрацию командой <code>/stopreg</code> или <code>'
                             '/stopreg baku</code>', parse_mode='HTML')


@dp.callback_query_handler(text="1t")
@dp.callback_query_handler(text='0t')
@dp.callback_query_handler(text="1b")
@dp.callback_query_handler(text='0b')
async def userPlaying(callback: types.CallbackQuery):
    if callback.data.endswith('b'):
        isTrue = False
    else:
        isTrue = True

    chatId = callback.message.chat.id

    if callback.from_user.username is None:
        name = callback.from_user.first_name
    else:
        name = f"@{callback.from_user.username}"

    if callback.data.startswith('1'):
        if name in getUsers(chatId, true=isTrue):
            await callback.answer("Ты уже в списке.")
        else:
            if not len(getUsers(chatId, true=isTrue)) > 1:
                addUsername(username=name, chatID=chatId, true=isTrue)
            else:
                addUsername(username=name, chatID=chatId, true=isTrue)
            await callback.answer()
    else:
        try:
            removeUsername(username=name, chatID=chatId, true=isTrue)
        except ValueError:
            await callback.answer('Тебя не было в списке.', show_alert=True)

    if isTrue:
        await bot.edit_message_text(message_id=getId(chatId=chatId, true=isTrue), chat_id=chatId, reply_markup=keyboardTrue,
                                    text=MafiaArray(getUsers(chatId, true=isTrue), captain=getCaptain(chatId, true=isTrue),
                                                   team=callback.message.chat.id, isTrue=isTrue))
    else:
        await bot.edit_message_text(message_id=getId(chatId=chatId, true=isTrue), chat_id=chatId, reply_markup=keyboardBaku,
                                    text=MafiaArray(getUsers(chatId, true=isTrue), captain=getCaptain(chatId, true=isTrue),
                                                   team=callback.message.chat.id, isTrue=isTrue))


@dp.message_handler(commands=['kick_from_list', 'kfl'], commands_prefix='!./#?')
async def remove_from_list(message: types.Message):
    try:
        username = message.text.split()[1]

        if not message.text.split()[-1] == username:
            if message.text.split()[-1] in values:
                isTrue = False
            else:
                isTrue = True
        else:
            isTrue = True

        try:
            removeUsername(username=username, chatID=message.chat.id, true=isTrue)
            await message.answer(f'{username} удален из списка.')
        except ValueError:
            await message.answer(f'{username} не было в списке.')

        chatId = message.chat.id
        if isTrue:
            await bot.edit_message_text(message_id=getId(chatId=chatId, true=isTrue), chat_id=chatId,
                                        reply_markup=keyboardTrue,
                                        text=MafiaArray(getUsers(chatId, true=isTrue),
                                                        captain=getCaptain(chatId, true=isTrue),
                                                        team=chatId, isTrue=isTrue))
        else:
            await bot.edit_message_text(message_id=getId(chatId=chatId, true=isTrue), chat_id=chatId,
                                        reply_markup=keyboardBaku,
                                        text=MafiaArray(getUsers(chatId, true=isTrue),
                                                        captain=getCaptain(chatId, true=isTrue),
                                                        team=chatId, isTrue=isTrue))
    except IndexError:
        await message.answer('<code>/kick_from_list USERNAME</code>, где USERNAME - имя пользователя человека '
                             'которого нужно удалить\nДля удаления из списка баку: <code>/kick_from_list USERNAME '
                             'Baku</code>', parse_mode='HTML')


@dp.message_handler(commands=['captain'], commands_prefix='/.!')
async def updateCaptainsUsername(message: types.Message):
    try:
        if message.text.split()[1] in values:
            isTrue = False
            try:
                captain = message.text.split()[2]
                if captain == 'me':
                    if message.from_user.username is not None:
                        captain = f"@{message.from_user.username}"
                    else:
                        captain = f'{message.from_user.first_name}'
            except IndexError:
                captain = "@captain"
        else:
            isTrue = True
            if (captain := message.text.split()[1]) == 'me':
                captain = f"@{message.from_user.username}"
            else:
                captain = captain
    except IndexError:
        isTrue = True
        captain = "@captain"
    chatId = message.chat.id

    updateCaptain(username=captain, chatID=message.chat.id, true=isTrue)
    if isTrue:
        await bot.edit_message_text(message_id=getId(chatId=chatId, true=isTrue), chat_id=chatId,
                                    reply_markup=keyboardTrue,
                                    text=MafiaArray(getUsers(chatId, true=isTrue),
                                                    captain=getCaptain(chatId, true=isTrue),
                                                    team=chatId, isTrue=isTrue))
    else:
        await bot.edit_message_text(message_id=getId(chatId=chatId, true=isTrue), chat_id=chatId,
                                    reply_markup=keyboardBaku,
                                    text=MafiaArray(getUsers(chatId, true=isTrue),
                                                    captain=getCaptain(chatId, true=isTrue),
                                                    team=chatId, isTrue=isTrue))


@dp.message_handler(commands=['stopreg', 'cancel'], commands_prefix='!/.')
async def stopRegistration(message: types.Message):
    try:
        if message.text.split()[1] in values:
            isTrue = False
        else:
            isTrue = True
    except IndexError:
        isTrue = True

    chatId = message.chat.id

    try:
        await bot.edit_message_text(chat_id=chatId, message_id=getId(chatId=chatId, true=isTrue),
                                    text=MafiaArray(getUsers(chatId, true=isTrue), captain=getCaptain(chatId, true=isTrue),
                                                    team=message.chat.id, isTrue=isTrue))
    except MessageToEditNotFound:
        await message.answer('Для остановки регистрации на баку используется команда <code>/stopreg baku</code>. '
                             'Также возможно, сообщение со регистрацией удалено, если так, используйте /stopanyway',
                             parse_mode='HTML')

    await message.answer(text=f'<a href="https://t.me/c/{str(chatId)[3:]}/{getId(chatId=chatId, true=isTrue)}">Список.</a>',
                         parse_mode='HTML')
    del_users_and_messageId(chatID=chatId, true=isTrue)
