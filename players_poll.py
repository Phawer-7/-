def trueMafia(usernames, captain='@captain'):
    # users = [i[0] for i in usernames]

    mydict = {
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

    res = ""

    for i, y in enumerate(usernames, 1):
        res = res + (mydict[i] + f' @{y}') + "\n"

    res = f'🎻 ʀᴇɴᴀɪssᴀɴᴄᴇ|{captain} 🌅\n\n{res}'
    return res


def bakuMafia(usernames, captain, last):
    # users = [i[0] for i in usernames]

    mydict = {
        1: "𝐑.",
        2: "𝐄.",
        3: "𝐕.",
        4: "𝐈.",
        5: "𝐓.",
        6: "𝐀.",
        7: "𝐋.",
        8: "𝐈.",
        9: "𝐙.",
        10: "𝐀.",
        11: "𝐓.",
        12: "𝐈.",
        13: "𝐎.",
        14: "𝐍.",
    }

    res = ""

    for i, y in enumerate(usernames, 1):
        res = res + (mydict[i] + f' @{y}') + "\n"

    res = f'🎻 ʀᴇɴᴀɪssᴀɴᴄᴇ | {captain} 🌅\n\n{res}\n🎻@{last}🌅'

    return res
