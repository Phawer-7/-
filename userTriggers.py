from localization import caps_normal_char, normal_char, personal_sendName
from simple import dp, types, bot
from manipulationWithName import returnWithoutSmiles
from mongoDB import usersNameExists
from user_triggers import createUserColl, userExists, createNewUserTrigger, updateUserTrigger, TriggerAlreadyExists, \
    getPersonalTriggerList


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


@dp.message_handler(commands=['mylist', 'mytriggers', 'my_triggers', 'my_list_triggers'], commands_prefix='/!.#')
async def sendPersonalTriggerList(message: types.Message):
    if getPersonalTriggerList(message.from_user.id) == 'Список личных триггеров:\n':
        await message.answer('У вас пока нет личных триггеров.')
    else:
        await message.answer(f'{getPersonalTriggerList(message.from_user.id)}')
