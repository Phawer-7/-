import emoji
from mongoDB import getTrigger, getDefaultTriggerChat


normal_char = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z",
               "x", "c", "v", "b", "n", "m", "й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы",
               "в", "а", "п", "р", "о", "л", "д", "ж", "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "/", "(", ")",
               " ", "\\", "'", '"', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "#",
               '_', '-', '&', '*', '%', "!", "?", "!", "^", "$", "ё", "қ", "ў", "'", "♡", "ғ", "ҳ"]

caps_normal_char = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                    'X', 'C', 'V', 'B', 'N', 'M', 'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф', 'Ы',
                    'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', "Ё", "Қ",
                    "Ў", "Ҳ", "Ғ"]


def send_name(chat_id, color, name='ник', default=False):
    try:
        if not default:
            listValue = getTrigger(collect_name=str(chat_id), trigger_name=color)
            if type(listValue) is list:
                x = emoji.emojize(f"{listValue[0]}")
                z = emoji.emojize(f"{listValue[1]}")
                return f"{x}{name}{z}"
            elif type(listValue) is str:
                return listValue
        else:
            listValue = getDefaultTriggerChat(collect_name=chat_id)['value']
            if type(listValue) is list:
                x = emoji.emojize(f"{listValue[0]}")
                z = emoji.emojize(f"{listValue[1]}")
                return f"{x}{name}{z}"
            elif type(listValue) is str:
                return listValue
    except KeyError:
        return f'🎻ʀᴇ|{name}🌅'
    except TypeError:
        return 'Такого триггера не существует'



