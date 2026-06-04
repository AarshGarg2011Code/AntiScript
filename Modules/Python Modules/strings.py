# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'strings'

def strings_upper(text):
    return str(text).upper()


def strings_lower(text):
    return str(text).lower()


def strings_title(text):
    return str(text).title()


def strings_length(text):
    return len(str(text))


def strings_contains(text, value):
    return str(value) in str(text)


def strings_replace(text, old, new):
    return str(text).replace(
        str(old),
        str(new)
    )


def strings_split(text, separator):
    return str(text).split(
        str(separator)
    )


def strings_startswith(text, prefix):
    return str(text).startswith(
        str(prefix)
    )


def strings_endswith(text, suffix):
    return str(text).endswith(
        str(suffix)
    )


def strings_reverse(text):
    return str(text)[::-1]