# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'ciphers'

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA 
from Crypto.Random import get_random_bytes
import base64

def caesar_encrypt(text, shift):
    result = ""

    for ch in text:
        if ch.isalpha():
            start = ord('A') if ch.isupper() else ord('a')
            result += chr(
                (ord(ch) - start + shift) % 26 + start
            )
        else:
            result += ch

    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def xor_encrypt(text, key):
    return ''.join(
        chr(ord(ch) ^ key)
        for ch in text
    )

def xor_decrypt(text, key):
    return xor_encrypt(text, key)

def base64_encode(text):
    return base64.b64encode(
        text.encode("utf-8")
    ).decode("utf-8")

def base64_decode(text):
    return base64.b64decode(
        text.encode("utf-8")
    ).decode("utf-8")

def atbash_encrypt(text):
    result = ""
    for ch in text:
        if ch.isupper():
            result += chr(
                ord('Z') - (ord(ch) - ord('A'))
            )
        elif ch.islower():
            result += chr(
                ord('z') - (ord(ch) - ord('a'))
            )
        else:
            result += ch
    return result

def atbash_decrypt(text):
    return atbash_encrypt(text)

def ascii_encrypt(text, shift):
    return ''.join(
        chr((ord(ch) + shift) % 256)
        for ch in text
    )

def ascii_decrypt(text, shift):
    return ''.join(
        chr((ord(ch) - shift) % 256)
        for ch in text
    )

def aes_generate_key():
    return get_random_bytes(32)  # 256-bit key

def aes_encrypt(text, key):
    cipher = AES.new(key, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(
        text.encode("utf-8")
    )

    data = (
        cipher.nonce +
        tag +
        ciphertext
    )

    return base64.b64encode(data).decode()

def aes_decrypt(ciphertext_b64, key):
    data = base64.b64decode(ciphertext_b64)

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(
        key,
        AES.MODE_EAX,
        nonce=nonce
    )

    plaintext = cipher.decrypt_and_verify(
        ciphertext,
        tag
    )

    return plaintext.decode()

def rsa_generate_keys(bits=2048):
    key = RSA.generate(bits)

    private_key = key.export_key().decode()

    public_key = (
        key.publickey()
        .export_key()
        .decode()
    )

    return public_key, private_key


def rsa_encrypt(text, public_key):
    key = RSA.import_key(public_key)

    cipher = PKCS1_OAEP.new(key)

    encrypted = cipher.encrypt(
        text.encode("utf-8")
    )

    return base64.b64encode(
        encrypted
    ).decode()


def rsa_decrypt(ciphertext_b64, private_key):
    key = RSA.import_key(private_key)

    cipher = PKCS1_OAEP.new(key)

    encrypted = base64.b64decode(
        ciphertext_b64
    )

    plaintext = cipher.decrypt(
        encrypted
    )

    return plaintext.decode()