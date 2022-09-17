def trueMafia(usernames, captain='@captain'):
    users = [i[0] for i in usernames]

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

    for i, y in enumerate(users, 1):
        res = res + (mydict[i]+f' @{y}') + "\n"

    res = f'🎻 ʀᴇɴᴀɪssᴀɴᴄᴇ|{captain} 🌅\n\n{res}'
    return res

