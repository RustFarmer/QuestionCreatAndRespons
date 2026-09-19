import json
from loguru import logger

from Settings.module import filename_url, log_settings_path
from Settings.UpdateProgram.GetFileUrl.getFileUrl import GetFileUrl

logger.add(f"{log_settings_path}save_urlLog.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


class SaveUrlFile:
    def __init__(self):
        self.filename = filename_url
        self.file_url = GetFileUrl().__load_url__
        print(self.file_url)

        logger.info(self.file_url)

    def save_url_file(self) -> bool | FileNotFoundError:
        try:
            data = dict(self.file_url)
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except FileNotFoundError as e:
            return e
