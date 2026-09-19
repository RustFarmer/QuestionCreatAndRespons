import json
import requests

from typing import Type
from loguru import logger

from Settings.JsonKey import requests_version_key
from Settings.module import filename_settings, version_url, log_settings_path

logger.add(f"{log_settings_path}checkVersionLog.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


class CheckVersionProgram:
    def __init__(self):
        self.version_url: str = version_url
        self.filename_settings: str = filename_settings
        self.requests_version: dict = self.__get_version__
        self.program_version: dict = self.__load_version__.get(requests_version_key)

        logger.info(self.version_url)
        logger.info(self.filename_settings)
        logger.info(self.requests_version)

    def __check_connection__(self) -> bool:
        try:
            response = requests.get(self.version_url)
            logger.info(response)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    @property
    def __get_version__(self) -> Type[ConnectionError] | dict | ConnectionError:
        try:
            if self.__check_connection__() is False:
                return ConnectionError
            return dict(json.loads(requests.get(self.version_url).text)).get(requests_version_key)
        except ConnectionError as e:
            return e

    @property
    def __load_version__(self) -> FileNotFoundError | dict:
        try:
            with open(self.filename_settings, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError as e:
            return e

    def __check_version__(self) -> Type[ConnectionError] | bool:
        if self.__check_connection__() is False:
            return ConnectionError

        logger.info(self.program_version)
        logger.info(self.requests_version)
        logger.info(self.program_version != self.version_url)

        if self.program_version < self.requests_version:
            return True
        return False
