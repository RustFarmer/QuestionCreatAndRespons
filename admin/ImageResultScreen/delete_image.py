import json
import os

from pathlib import Path

from fileModule import FileNameAdmin, FileNameClient


class DeleteImage:
    def __init__(self, image_path_client=FileNameClient.filename_CLINET_image_settings,
                 filename_settings=FileNameAdmin.filename_image_settings,
                 image_path=FileNameAdmin.image_path):
        self.image_path = image_path
        self.filename_settings = filename_settings
        self.image_path_client = image_path_client
        self.image_name = None

    def get_name_image(self, image_id: int):
        with open(self.filename_settings, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            ImageDataId = item["Image"]["image_id"]
            if ImageDataId == image_id:
                return item["Image"].get("image_name")

    def del_recording_in_json(self, image_id):
        try:
            with open(self.filename_settings, 'r', encoding='utf-8') as f:
                data = json.load(f)
            new_data = [u for u in data if u["Image"]["image_id"] != image_id]
            with open(self.filename_settings, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)

        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            with open(self.filename_settings, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def del_image(self, image_id: int):
        file_path = Path(f'{self.image_path}\\{self.get_name_image(image_id)}')
        print(file_path)
        self.del_recording_in_json(image_id)
        print(file_path.is_file())
        if file_path.is_file():
            file_path.unlink()
