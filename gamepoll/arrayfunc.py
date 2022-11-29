from gamepoll.addingList import getListPeaces
from gamepoll.arraySamples import mainPiece

resurgence = {
    1: "𝐑",
    2: "𝐄",
    3: "𝐒",
    4: "𝐔",
    5: "𝐑",
    6: "𝐆",
    7: "𝐄",
    8: "𝐍",
    9: "𝐂",
    10: "𝐄"
}

doesNotExists = {
    1: "1 {0}",
    2: "2 {0}",
    3: "3 {0}",
    4: "4 {0}",
    5: "5 {0}",
    6: "6 {0}",
    7: "7 {0}",
    8: "8 {0}",
    9: "9 {0}",
    10: "10 {0}"
}

doesNotExistsBaku = {
    1: "1 {0}",
    2: "2 {0}",
    3: "3 {0}",
    4: "4 {0}",
    5: "5 {0}",
    6: "6 {0}",
    7: "7 {0}",
    8: "8 {0}",
    9: "9 {0}",
    10: "10 {0}",
    11: "11 {0}",
    12: "12 {0}",
    13: "13 {0}",
    14: "14 {0}",
    15: "15 {0}"
}

fifi = {
    1: "           1.",
    2: "                     2.",
    3: "     3.",
    4: "                4.",
    5: "5.",
    6: "              6.",
    7: "                         7.",
    8: "      8.",
    9: "                 9.",
    10: "10."
}


freeWill = {
    1: "𓂃 ᜊ {0}  ⋆←,",
    2: "            𓂃 𖧷 {0}  𓂅",
    3: "                        𓂃 ໒ {0}  ⋆←,",
    4: "𓂃 ᜊ {0}  ⋆←,",
    5: "            𓂃 𖧷 {0}  𓂅",
    6: "                        𓂃 ໒ {0} ⋆←,",
    7: "𓂃 ᜊ {0}  ⋆←,",
    8: "            𓂃 𖧷 {0} 𓂅",
    9: "                        𓂃 ໒ {0}  ⋆←,",
    10: "𓂃 ᜊ {0}  ⋆←,"
}

freeWillBaku = {
    1: "𓂃 ᜊ {0}  ⋆←,",
    2: "            𓂃 𖧷 {0}  𓂅",
    3: "                        𓂃 ໒ {0}  ⋆←,",
    4: "𓂃 ᜊ {0}  ⋆←,",
    5: "            𓂃 𖧷 {0}  𓂅",
    6: "                        𓂃 ໒ {0} ⋆←,",
    7: "𓂃 ᜊ {0}  ⋆←,",
    8: "            𓂃 𖧷 {0} 𓂅",
    9: "                        𓂃 ໒ {0}  ⋆←,",
    10: "𓂃 ᜊ {0}  ⋆←,",
    11: "            𓂃 𖧷 {0} 𓂅",
    12: "                        𓂃 ໒ {0}  ⋆←,",
    13: "𓂃 ᜊ {0}  ⋆←,",
    14: "            𓂃 𖧷 {0}  𓂅",
    15: "                        𓂃 ໒ {0}  ⋆←"
}


memento_mori = {
    "𝚖 —  {}",
    "𝚎 —  {}",
    "𝚖 —  {}",
    "𝚎 —  {}",
    "𝚗 —  {}.  𝒄𝒂𝒑𝒕𝒂𝒊𝒏",
    "𝚝 —  {}",
    "ō —  {}}",
    "𝚖 —  {}",
    "𝚘 —  {}",
    "𝚛 —  {}"
}


def MafiaArray(usernames, isTrue, captain='@captain', team=0):
        if isTrue:
            bot = 'True'
            list_game = doesNotExists
        else:
            bot = 'Baku'
            list_game = doesNotExistsBaku

        res = ""
        maxlen = len(usernames)
        if not type(usernames) == bool:
            if not mainPiece(chat_id=team, bot=bot) is None:
                for i in range(1, len(mainPiece(chat_id=team, bot=bot).values()) + 1):
                    if i > maxlen:
                        break
                    else:
                        res = f"{res}\n{mainPiece(chat_id=team, bot=bot)[i].format(usernames[i - 1])}"

                res = f'{getListPeaces(chat_id=team, opening=True, bot=bot).format(captain)}\n{res}\n' \
                      f'{getListPeaces(chat_id=team, ending=True, bot=bot)}'
                return res
            else:
                for i in range(1, len(list_game.values()) + 1):
                    if i > maxlen:
                        break
                    else:
                        res = f"{res}\n{list_game[i].format(usernames[i - 1])}"

                res = f'Cap: {captain}\n{res}'
                return res
