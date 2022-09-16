import emoji

normal_char = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z",
               "x", "c", "v", "b", "n", "m", "й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы",
               "в", "а", "п", "р", "о", "л", "д", "ж", "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "/", "(", ")",
               " ", "\\", "'", '"', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "#",
               '_', '-', '&', '*', '%', "!", "?", "!", "^", "$", "ё", "қ", "ў", "'",]

caps_normal_char = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                    'X', 'C', 'V', 'B', 'N', 'M', 'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф', 'Ы',
                    'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', "Ё", "Қ",
                    "Ў"]


def send_name(name='Kamol', color='белый', user_id=000000, dictt=False):
    global nick
    nick = {
        "черный": emoji.emojize(f':black_circle:🎻ʀᴇ|{name}🌅'),
        "чёрный": emoji.emojize(f':black_circle:🎻ʀᴇ|{name}🌅'),
        "black": emoji.emojize(f':black_circle:🎻ʀᴇ|{name}🌅'),
        "желтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|{name}🌅'),
        "yellow": emoji.emojize(f':yellow_circle:🎻ʀᴇ|{name}🌅'),
        "жёлтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|{name}🌅'),
        'мизан': emoji.emojize(f'𝖑𝖎𝖗||{name}'),
        'мизантроп': emoji.emojize(f':black_circle:𝖑𝖎𝖗||{name}'),
        "белый": emoji.emojize(f':white_circle:🎻ʀᴇ|{name}🌅'),
        "white": emoji.emojize(f':white_circle:🎻ʀᴇ|{name}🌅'),
        "ktm": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{name}🐈'),
        "katsu": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{name}🐈'),
        "катсу": emoji.emojize(f'🏮༄𝑲𝑻𝑴|{name}🐈'),
        "нюдсы": emoji.emojize(f'💃🏻ɴ |{name}🦇'),
        "бабочки": emoji.emojize(f'🖤𝐛𝐮𝐭𝐭|{name}🦋'),
        "баттерфлай": emoji.emojize(f'🖤𝐛𝐮𝐭𝐭|{name}🦋'),
        "butterfly": emoji.emojize(f'🖤𝐛𝐮𝐭𝐭|{name}🦋'),
        "розы": emoji.emojize(f'🥀𝐖𝐑𝐓 |{name}🌹'),
        "уилтед": emoji.emojize(f'🥀𝐖𝐑𝐓 |{name}🌹'),
        "rose": emoji.emojize(f'🥀𝐖𝐑𝐓 |{name}🌹'),
        "wilted": emoji.emojize(f'🥀𝐖𝐑𝐓 |{name}🌹'),
        "charged": emoji.emojize(f'𝗖𝗧🦾|{name}🧑‍🏭'),
        "чаржед": emoji.emojize(f'𝗖𝗧🦾|{name}🧑‍🏭'),
        "чаргет": emoji.emojize(f'𝗖𝗧🦾|{name}🧑‍🏭'),
        "сварщики": emoji.emojize(f'𝗖𝗧🦾|{name}🧑‍🏭'),
        "сварщик": emoji.emojize(f'𝗖𝗧🦾|{name}🧑‍🏭'),
    }

    malik = {
        "белый": emoji.emojize(f':white_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        "white": emoji.emojize(f':white_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        "черный": emoji.emojize(f':black_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        "black": emoji.emojize(f':black_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        "чёрный": emoji.emojize(f':black_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        "желтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        "жёлтый": emoji.emojize(f':yellow_circle:🎻ʀᴇ|:joystick:{name}:musical_note:🌅'),
        'мизан': emoji.emojize(f'𝖑𝖎𝖗||{name}'),
        'мизантроп': emoji.emojize(f':black_circle:𝖑𝖎𝖗||{name}'),
        "ktm": emoji.emojize(f'🏮༄𝑲𝑻𝑴|:joystick:{name}:musical_note:🐈'),
        "katsu": emoji.emojize(f'🏮༄𝑲𝑻𝑴|:joystick:{name}:musical_note:🐈'),
        "катсу": emoji.emojize(f'🏮༄𝑲𝑻𝑴|:joystick:{name}:musical_note:🐈'),
        "нюдсы": emoji.emojize(f'💃🏻ɴ |:joystick:{name}:musical_note:🦇'),
        "бабочки": emoji.emojize(f'🖤𝐛𝐮𝐭𝐭|:joystick:{name}:musical_note:🦋'),
        "баттерфлай": emoji.emojize(f'🖤𝐛𝐮𝐭𝐭|:joystick:{name}:musical_note:🦋'),
        "butterfly": emoji.emojize(f'🖤𝐛𝐮𝐭𝐭|:joystick:{name}:musical_note:🦋'),
        "розы": emoji.emojize(f'🥀𝐖𝐑𝐓 |:joystick:{name}:musical_note:🌹'),
        "уилтед": emoji.emojize(f'🥀𝐖𝐑𝐓 |:joystick:{name}:musical_note:🌹'),
        "rose": emoji.emojize(f'🥀𝐖𝐑𝐓 |:joystick:{name}:musical_note:🌹'),
        "wilted": emoji.emojize(f'🥀𝐖𝐑𝐓 |:joystick:{name}:musical_note:🌹'),
        "charged": emoji.emojize(f'𝗖𝗧🦾|:joystick:{name}:musical_note:🧑‍🏭'),
        "чаржед": emoji.emojize(f'𝗖𝗧🦾|:joystick:{name}:musical_note:🧑‍🏭'),
        "чаргет": emoji.emojize(f'𝗖𝗧🦾|:joystick:{name}:musical_note:🧑‍🏭'),
        "сварщики": emoji.emojize(f'𝗖𝗧🦾|:joystick:{name}:musical_note:🧑‍🏭'),
        "сварщик": emoji.emojize(f'𝗖𝗧🦾|:joystick:{name}:musical_note:🧑‍🏭'),
    }

    if dictt:
        list_of_trig = [i for i, o in nick.items()]
        return "\n".join(list_of_trig)
    else:
        try:
            if user_id == 819411604:
                return malik[color]
            else:
                return nick[color]
        except KeyError:
            return 'Такого триггера не существует'
