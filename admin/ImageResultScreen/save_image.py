import json

from fileModule import FileNameAdmin, FileNameClient


class SaveImage:
    def __init__(self, image_id_=False, filename=FileNameAdmin.filename_image_settings):
        self.dict_d = None
        self.image_name = None
        self.filename = filename
        if image_id_:
            self.image_id = image_id_
        else:
            self.image_id = self.qs_id()

    def dict(self) -> dict:
        json_dict = {
            "Image": {
                "image_name": self.image_name,
                "image_id": self.image_id
            }
        }
        return json_dict

    def qs_id(self) -> int:
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            last_id = 0
        else:
            last_items = data[-1]
            last_id = last_items["Image"]["image_id"]
        self.image_id = last_id + 1
        return self.image_id

    def save(self, image_name):

        self.image_name = image_name
        self.dict_d = self.dict()

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = list(data) + [self.dict_d]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            return e
