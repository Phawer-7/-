from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config import mongo

client = MongoClient(mongo, connect=False, server_api=ServerApi('1'))
db = client.Girolamo


def createColl(chat_id: int, name: str):
    coll = db[str(chat_id)]
    coll.insert_one({'_id': 1, 'name': name, 'group_id': chat_id})
    coll.insert_one({'_id': 2, 'name': 'ренессанс', 'value': ['🎻ʀᴇ|', '🌅']})


def createNewTrigger(collect_name, trigger_name: str, trigger_value: list):
    coll = db[str(collect_name)]
    coll.insert_one({'_id': coll.count_documents({})+1, 'name': trigger_name, 'value': trigger_value})


def getTrigger(collect_name, trigger_name: str):
    coll = db[str(collect_name)]
    query = {'name': trigger_name}

    return coll.find_one(query, {"value": 1})['value']


def setDefaultTriggerChat(collect_name, trigger_name: str, trigger_value: list):
    coll = db[str(collect_name)]
    coll.insert_one({'_id': coll.count_documents({})+1, 'name': trigger_name, 'value': trigger_value,
                     'default_trigger': True})


def setDefaultNameUser(user_id: int, name: str, username: str, telegram_name: str):
    coll = db['users']
    coll.insert_one({'_id': coll.count_documents({})+1, 'name': name, 'telegram-id': user_id,
                     'telegram-name': telegram_name, 'telegram-username': username})


def getTriggerList(collect_name):
    coll = db[str(collect_name)]
    triggerList = ''
    for i in coll.find_one()['name']:
        triggerList = f'{triggerList}{i}'

    return triggerList
