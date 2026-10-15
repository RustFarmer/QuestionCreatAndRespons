import os
from pathlib import Path


def get_client_path() -> Path:
    return Path(__file__).resolve().parent


def get_all_file_in_path():
    all_file = []
    path = '.'
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            all_file.append(name)
            print('File:', name)
    return all_file


def get_absolute_path() -> Path:
    return Path(__file__).resolve().parent
