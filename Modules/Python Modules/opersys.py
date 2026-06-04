# AntiScript v1.0.0
# Made by Aarsh Garg in 2026.
# Module 'opersys'

import os

def opersys_cwd():
    return os.getcwd()

def opersys_exists(path):
    return os.path.exists(path)

def opersys_mkdir(path):
    os.makedirs(
        str(path),
        exist_ok=True
    )

def opersys_listdir(path="."):
    return os.listdir(path)

def opersys_remove(path):
    os.remove(path)

def opersys_rename(old, new):
    os.rename(old, new)

def opersys_getenv(name):
    return os.getenv(name)