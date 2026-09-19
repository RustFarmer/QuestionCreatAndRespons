import json

from Settings.module import filename_url
from Settings.JsonKey import rarFile


class getFileUrlForDownload:
    def __init__(self):
        self.filename_url = filename_url

    @property
    def get_url(self) -> str | FileNotFoundError:
        try:
            with open(self.filename_url, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(rarFile)
        except FileNotFoundError as e:
            return e

