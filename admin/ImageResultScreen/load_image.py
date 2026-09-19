import json
import os

from pathlib import Path
from PIL import Image

from fileModule import FileNameAdmin, FileNameClient


class LoadImage:
    def __init__(self, image_path_client=FileNameClient.filename_CLINET_image_settings,
                 filename_settings=FileNameAdmin.filename_image_settings,
                 image_path=FileNameAdmin.image_path):
        self.image_path = image_path
        self.filename_settings = filename_settings
        self.image_path_client = image_path_client
        self.folder_path = Path(self.image_path_client)
        self.image_name = None

    def load_image(self, image_id):
        self.del_old_image()
        with open(self.filename_settings, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for x in data:
            image_data = x.get('Image')
            if image_data.get('image_id') == image_id:
                image_name = image_data.get('image_name')
                self.image_name = image_name

                source_path = Path(self.image_path) / image_name

                dest_dir = Path(self.image_path_client)
                dest_dir.mkdir(parents=True, exist_ok=True)

                dest_path = dest_dir / image_name

                img = Image.open(source_path)
                img.save(dest_path)

    def del_old_image(self):
        folder_path = Path(self.image_path_client)
        for item in folder_path.iterdir():
            if item.is_file():
                os.remove(str(item))
