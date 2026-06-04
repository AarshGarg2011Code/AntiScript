# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'system'

def system_typeof(value):

    if isinstance(value, bool):
        return "truth"

    if isinstance(value, int):
        return "number"

    if isinstance(value, float):
        return "decimal"

    if isinstance(value, str):
        return "text"

    if isinstance(value, list):
        return "list"

    return "unknown"


def system_version():
    return "AntiScript v1.0.0"


def system_author():
    return "Aarsh Garg"


def system_repeat(text, count):
    return str(text) * int(count)


def system_newline():
    return "\n"
    
def system_abort():
    exit()

def system_pause(text):
    pause = input(text)