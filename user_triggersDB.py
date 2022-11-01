from mongoDB import client

from pymongo import errors

users_database = client.user_triggers


def createUserColl(user_id: int, name: str, username: str):
    coll = users_database[str(user_id)]
    coll.insert_one({'_id': 1, 'name': name, 'user-id': user_id, 'telegram-username': username})


def userExists(user_id: int):
    coll = users_database[str(user_id)]

    if not coll.find_one({'user-id': user_id}) is None:
        return coll.find_one({'user-id': user_id})['user-id']
    else:
        return False


def createNewUserTrigger(user_id: int, trigger_name: str, trigger_value: list):
    coll = users_database[str(user_id)]

    try:
        coll.insert_one({'_id': coll.count_documents({}) + 1, 'user-id': user_id, 'trigger-name': trigger_name,
                         'value': trigger_value, 'is_active': True})
    except errors.DuplicateKeyError:
        coll.insert_one({'_id': coll.count_documents({}) + 2, 'user-id': user_id, 'trigger-name': trigger_name,
                         'value': trigger_value, 'is_active': True})


def getUserTrigger(user_id: int, trigger_name=str) -> list:
    coll = users_database[str(user_id)]

    query = {'trigger-name': trigger_name}

    if coll.find_one(query, {"value": 1}):
        return coll.find_one(query, {"value": 1})['value']
    else:
        return 0


def TriggerAlreadyExists(user_id: int, name: str):
    coll = users_database[str(user_id)]

    if not coll.find_one({'trigger-name': name}) is None:
        return coll.find_one({'trigger-name': name})['trigger-name']
    else:
        return False


def updateUserTrigger(user_id: int, trigger_name: str, trigger_value: list):
    coll = users_database[str(user_id)]

    old_data = {'trigger-name': trigger_name}
    new_data = {'$set': {'value': trigger_value, 'is_active': True}}

    coll.update_one(old_data, new_data)


def getPersonalTriggerList(collect_name):
    coll = users_database[str(collect_name)]
    triggerList = 'Список личных триггеров:\n'
    for i in coll.find():
        try:
            if not 'is_active' in list(i.keys()):
                triggerList = f"{triggerList}{i['trigger-name']}\n"
            if i['is_active']:
                triggerList = f"{triggerList}{i['trigger-name']}\n"
        except KeyError:
            pass

    return triggerList


def deleteUserTrigger(user_id: int, trigger_name: str):
    coll = users_database[str(user_id)]

    old_data = {'trigger-name': trigger_name}
    new_data = {'$set': {'is_active': False}}

    return coll.update_one(old_data, new_data)


def triggerUserExists(user_id: int, trigger_name: str):
    coll = users_database[str(user_id)]
    if not coll.find_one({'trigger-name': trigger_name}) is None:
        return coll.find_one({'trigger-name': trigger_name})['value']
    else:
        return False
