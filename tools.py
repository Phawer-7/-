def textWithoutCommand(text: str) -> str:
    cmd = text.split()[0]
    text = text.replace(cmd, "").lstrip()

    if len(text) == 0:
        return None
    else:
        return text
