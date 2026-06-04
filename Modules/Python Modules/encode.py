# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'encode'

def encode_ascii(text: str):
    char_ascii = []
    for ch in text:
        char_ascii.append(str(ord(ch)))
    return char_ascii
    
def encode_binary(text: str):
    char_bin = []
    for ch in text:
        char_ascii.append(str(bin(ord(ch))))
    return char_bin
    
def encode_hexdec(text: str):
    char_hex = []
    for ch in text:
        char_ascii.append(str(hex(ord(ch))))
    return char_hex
    
def encode_unicode(text: str):
    char_uni = []
    for ch in text:
        ascii = ord(ch)
        char_uni.append(f"U+{ascii:04X}")
    return char_uni
    
def encode_finden(char: str):
    if len(char) == 1:
        print(f"Encodings for {char}")
        print(f" ASCII: {str(ord(char))}")
        print(f" Binary: {bin(ord(char))}")
        print(f" Hexadecimal: {hex(ord(char))}")
        ascii = ord(char)
        unicode = f"U+{ascii:04X}"
        print(f" Unicode: {unicode}")
    else:
        print("Argument can not exceed one character.")