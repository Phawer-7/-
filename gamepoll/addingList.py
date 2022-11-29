from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from gamepoll.arraySamples import mainPiece
from simple import dp
from mongoDB import client


class PlayList(StatesGroup):
    chat = State()
    opening = State()
    main = State()
    ending = State()


db = client.list


def create_list(chat_id: int, opening: str = '', ending: str = '', main: str = '', bot: str = 'True') -> bool:
    coll = db[str(bot)]
    if not coll.find_one({"chat_id": chat_id, 'bot': bot}) is None:
        new = {"$set": {"chat_id": chat_id, 'opening': opening, 'main': main, 'ending': ending, 'bot': bot}}
        coll.update_one({"chat_id": chat_id, 'bot': bot}, new)
    else:
        coll.insert_one({"_id": coll.count_documents({}) + 1, "chat_id": chat_id, 'opening': opening, 'main': main,
                         'ending': ending, 'bot': bot})


def _list(chat_id: int, opening: str = '', ending: str = '', main: str = '', bot: str = 'True') -> bool:
    coll = db[str(bot)]
    coll.insert_one({"_id": coll.count_documents({}) + 1, "chat_id": chat_id, 'opening': opening, 'main': main,
                     'ending': ending, 'bot': bot})


def getListPeaces(chat_id: int, opening: bool = False, ending: bool = False, main: bool = False, bot: str = 'True'):
    coll = db[str(bot)]
    res = coll.find_one({"chat_id": chat_id, 'bot': bot})

    textParts = {
        0: "opening",
        1: "ending",
        2: "main"
    }

    if not res is None:
        return res[textParts[[opening, ending, main].index(True)]]


@dp.message_handler(commands=['add_list'], commands_prefix='!/.#?', state="*")
async def addList(message: types.Message, state: FSMContext):
    if not message.chat.type == 'private':
        await message.answer('Команда работает только в личных чатах.')
    else:
        try:
            await message.answer("Выберите начала списка:")
            await state.set_state(PlayList.opening.state)
        except IndexError:
            await message.answer('<code>/add_list [chat_id]</code>, где [chat_id] - уникальный идентификатор '
                                 'чата. Узнать его можно использовав команду /get_chat_id в командной группе.',
                                 parse_mode='HTML')


@dp.message_handler(state=PlayList.opening)
async def opening_chosen(message: types.Message, state: FSMContext):
    await state.update_data(opening=message.text)
    await message.answer("Теперь выберете главную часть:")
    await state.set_state(PlayList.main.state)


@dp.message_handler(state=PlayList.main)
async def main_piece_chosen(message: types.Message, state: FSMContext):
    await state.update_data(main=message.text)
    await message.answer("Теперь выберете конец списка:")
    await state.set_state(PlayList.ending.state)


@dp.message_handler(state=PlayList.ending)
async def ending_chosen(message: types.Message, state: FSMContext):
    await state.update_data(ending=message.text)
    await message.answer('Введите <code>[chat_id]</code>, где [chat_id] - уникальный идентификатор чата. '
                         'Узнать его можно использовав команду /get_chat_id в командной группе.', parse_mode='HTML')
    await state.set_state(PlayList.chat.state)


@dp.message_handler(state=PlayList.chat)
async def chat_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    create_list(chat_id=int(message.text), opening=user_data['opening'], main=user_data['main'],
                ending=user_data['ending'], bot='True')

    await message.answer(f"{user_data['opening']}.\n{user_data['main']}\n{user_data['ending']}")
    await state.finish()

