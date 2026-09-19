import json
import requests

from loguru import logger
from Settings.module import file_data_url, log_settings_path

logger.add(f"{log_settings_path}GetfileUrl.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


class GetFileUrl:
    def __init__(self):
        self.file_url: str = file_data_url
        self.file_url_list: dict = self.__load_url__

        logger.info(self.file_url)
        logger.info(self.file_url_list)

    @property
    def __load_url__(self) -> dict:
        return dict(json.loads(requests.get(self.file_url).text))


