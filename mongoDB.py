from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from config import mongo

client = MongoClient(mongo)
chats = client.Girolamo


def createColl(chat_id: int, name: str):
    coll = chats[str(chat_id)]
    coll.insert_one({'_id': 1, 'name': name, 'group_id': chat_id})
    coll.insert_one({'_id': 2, 'name': 'ренессанс', 'value': ['🎻ʀᴇ|', '🌅'], 'is_active': True})


def createNewTrigger(collect_name, trigger_name: str, trigger_value: list):
    coll = chats[str(collect_name)]
    try:
        coll.insert_one({'_id': coll.count_documents({})+1, 'name': trigger_name, 'value': trigger_value,
                         'is_active': True})
    except DuplicateKeyError:
        coll.insert_one({'_id': coll.count_documents({})+2, 'name': trigger_name, 'value': trigger_value,
                         'is_active': True})


def updateChatTrigger(chatId: int, trigger_name: str, trigger_value: list):
    coll = chats[str(chatId)]

    old_name = {'name': trigger_name}
    new = {'$set': {'value': trigger_value, 'is_active': True}}

    coll.update_one(old_name, new)


def getTriggerList(collect_name):
    coll = chats[str(collect_name)]
    triggerList = 'Список триггеров чата:\n'
    for i in coll.find():
        try:
            if not 'is_active' in list(i.keys()):
                triggerList = f"{triggerList}{i['name']}\n"
            if i['is_active']:
                triggerList = f"{triggerList}{i['name']}\n"
        except KeyError:
            pass

    if triggerList == 'Список триггеров чата:\n':
        return 'У вас нет триггеров.'
    else:
        return triggerList


def getTrigger(collect_name, trigger_name: str):
    coll = chats[str(collect_name)]
    query = {'name': trigger_name}

    if coll.find_one(query, {"value": 1}):
        return coll.find_one(query, {"value": 1})['value']
    else:
        return 0


def triggerChatExists(chatId: int, trigger_name: str):
    coll = chats[str(chatId)]
    if not coll.find_one({'name': trigger_name}) is None:
        return coll.find_one({'name': trigger_name})['value']
    else:
        return False


def deleteChatTrigger(chatId: int, trigger_name: str):
    coll = chats[str(chatId)]

    oldData = {'name': trigger_name}
    new = {'$set': {'is_active': False}}

    coll.update_one(oldData, new)


def setDefaultNameUser(user_id: int, name: str, username: str, telegram_name: str):
    coll = chats['users']
    coll.insert_one({'_id': coll.count_documents({})+1, 'name': name, 'telegram-id': user_id,
                     'telegram-name': telegram_name, 'telegram-username': username})


def usersNameExists(user_id: int):
    coll = chats['users']
    if not coll.find_one({'telegram-id': user_id}) is None:
        return coll.find_one({'telegram-id': user_id})['name']
    else:
        return False


def updateDefaultNameUser(user_id: int, name: str):
    coll = chats['users']

    old_name = {'telegram-id': user_id}
    new = {'$set': {'name': name}}

    coll.update_one(old_name, new)


def defaultSmilesAreadyExists(chat_id):
    coll = chats['default']
    if not coll.find_one({'chat-id': chat_id}) is None:
        return coll.find_one({'chat-id': chat_id})['chat-id']
    else:
        return False


def updateDefaultSmilesChat(chat_id: int, default_trigger: list):
    coll = chats['default']

    old_name = {'chat-id': chat_id}
    new = {'$set': {'value': default_trigger}}

    coll.update_one(old_name, new)


def setDefaultTriggerChat(chat_id, chatName: str, trigger_value):
    coll = chats['default']
    try:
        coll.insert_one({'_id': coll.count_documents({})+1, 'chat-id': chat_id, 'value': trigger_value,
                        'chat-name': chatName})
    except DuplicateKeyError:
        coll.insert_one({'_id': coll.count_documents({})+2, 'chat-id': chat_id, 'value': trigger_value,
                         'chat-name': chatName})


def getDefaultTriggerChat(collect_name):
    coll = chats['default']
    if not coll.find_one({'chat-id': int(collect_name)}) is None:
        query = {'chat-id': collect_name}
        return coll.find_one(query, {"value": 1})
    else:
        return False


def getDefaultTriggerList():
    coll = chats['default']

    DefaultTriggerList = []

    for i in coll.find():
        try:
            DefaultTriggerList.append(i['value'])
        except KeyError:
            pass

    return DefaultTriggerList
