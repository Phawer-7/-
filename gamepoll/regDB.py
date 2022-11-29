from mongoDB import client
from pymongo.errors import DuplicateKeyError

tempD = client.temp_files
tempColl = tempD['message_id']


def addMessageId(message_id: int, chatName: str, chatId: int, captain: str, true=True):
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl
    try:
        tempColl2.insert_one({'_id': tempColl2.count_documents({})+1, "message_id": message_id, "Chat": chatName,
                              "ChatID": chatId, 'users': [], 'captain': captain})
    except DuplicateKeyError:
        tempColl2.insert_one({'_id': tempColl2.count_documents({})+2, "message_id": message_id, "Chat": chatName,
                             "ChatID": chatId, 'users': [], 'captain': captain})


def getUsers(chatID: int, true=True) -> list:
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    res = tempColl2.find_one({"ChatID": chatID})['users']

    if not res is None:
        return res
    else:
        return []


def addUsername(username: str, chatID: int, true=True):
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl
    arrlist = getUsers(chatID=chatID, true=true)
    old = {"ChatID": chatID}
    if not arrlist is None:
        arrlist.append(username)
        new = {"$set": {'users': arrlist}}
    else:
        new = {"$set": {'users': [username]}}

    tempColl2.update_one(old, new)


def removeUsername(username: str, chatID: int, true=True):
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    arrlist = getUsers(chatID=chatID, true=true)
    arrlist.remove(username)
    old = {"ChatID": chatID}
    new = {"$set": {'users': arrlist}}
    tempColl2.update_one(old, new)


def getId(chatId: int, true=True) -> int:
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    if not tempColl2.find_one({"ChatID": chatId}) is None:
        return tempColl2.find_one({"ChatID": chatId})["message_id"]

    else:
        return 'do not exists'


def getCaptain(chatID: int, true=True) -> str:
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    res = tempColl2.find_one({"ChatID": chatID})["captain"]

    if not res is None:
        return res
    else:
        return False


def updateCaptain(username: str, chatID: int, true=True):
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    old = {"ChatID": chatID}
    new = {"$set": {'captain': username}}
    tempColl2.update_one(old, new)


def del_users_and_messageId(chatID: int, true=True):
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    old = {"ChatID": chatID}
    new = {"$set": {'captain': '@captain', 'message_id': 0, "users": []}}

    tempColl2.update_one(old, new)


def updateMessageId(chatID: int, message_id: int, true=True):
    if not true:
        tempColl2 = tempD['message_idBAKU']
    else:
        tempColl2 = tempColl

    old = {"ChatID": chatID}
    new = {"$set": {'message_id': message_id}}

    tempColl2.update_one(old, new)
