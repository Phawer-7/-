from gamepoll.addingList import getListPeaces


def mainPiece(chat_id: int, bot: str = 'True') -> dict:
    if bot == 'True':
        text1 = getListPeaces(chat_id=chat_id, main=True)
    else:
        text1 = getListPeaces(chat_id=chat_id, main=True, bot='Baku')

    if not text1 is None:
        list_dict = {}
        for i in range(1, len(text1)+1):
            list_dict[i] = text1[i-1]

        res_dict = {}
        temp_str = ''
        for elem in list_dict.values():
            if not elem == '\n':
                temp_str = f'{temp_str}{elem}'
            else:
                res_dict[len(res_dict.keys())+1] = temp_str
                temp_str = ''
        return res_dict
