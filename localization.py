import emoji
from mongoDB import getTrigger


normal_char = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z",
               "x", "c", "v", "b", "n", "m", "й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы",
               "в", "а", "п", "р", "о", "л", "д", "ж", "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "/", "(", ")",
               " ", "\\", "'", '"', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "#",
               '_', '-', '&', '*', '%', "!", "?", "!", "^", "$", "ё", "қ", "ў", "'", "♡", "ғ", "ҳ"]

caps_normal_char = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                    'X', 'C', 'V', 'B', 'N', 'M', 'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф', 'Ы',
                    'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', "Ё", "Қ",
                    "Ў", "Ҳ", "Ғ"]


def send_name(chat_id, name='ник', color='белый', user_id=000000, return_dict=False):
    try:
        listValue = getTrigger(collect_name=str(chat_id), trigger_name=color)
        x = emoji.emojize(f"{listValue[0]}")
        z = emoji.emojize(f"{listValue[1]}")

        if user_id == 819411604:
            return f"{x}{emoji.emojize(':joystick:')}{name}{emoji.emojize(':musical_note:')}{z}"
        elif user_id == 785644394:
            return f"{x}{'𝐭𝐢𝐦𝐚'}{z}"
        else:
            return f"{x}{name}{z}"
    except KeyError:
        return 'Такого триггера не существует'
    except TypeError:
        return 'Такого триггера не существует'
