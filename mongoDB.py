from pymongo import MongoClient
from config import mongo

client = MongoClient(mongo)
db = client.Girolamo


def createColl(chat_id: int, name: str):
    coll = db[str(chat_id)]
    coll.insert_one({'_id': 1, 'name': name, 'group_id': chat_id})


def createNewTrigger(collect_name, trigger_name: str, trigger_value: list):
    coll = db[str(collect_name)]
    coll.insert_one({'_id': coll.count_documents({})+1, 'name': trigger_name, 'value': trigger_value})


def getTrigger(collect_name, trigger_name: str):
    coll = db[str(collect_name)]
    query = {'name': trigger_name}

    return coll.find_one(query, {"value": 1})['value']

