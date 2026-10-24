import json
from pathlib import Path

from loguru import logger


def get_absolute_path() -> Path:
    try:
        return Path(__file__).resolve().parent
    except FileNotFoundError:
        return Path(f'{Path(__file__).resolve().parent}\\_internal')


def get_client_path(flag=True):
    return Path(f'{get_absolute_path().parent}\\client\\')
    # else:
    # return Path(f'{get_absolute_path().parent.parent}\\client\\_internal')


logger.add(f"{get_absolute_path()}\\Log\\FirstRunfile.log",
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


def get_absolute_client_path() -> Path:
    return get_client_path()


def get_client_in_all_path() -> Path:
    return Path(f'{get_absolute_path().parent}\\ResponseInAll')


class FirstRun:
    def __init__(self):
        self.file_path_admin = get_absolute_path()
        self.client_path = get_client_path(True)
        print(self.client_path)
        self.filename_list_dict = {
            "\\Cookie\\local_cookie.json":
                {
                    "Body": {
                        "time_check_updates": "17:22 22.08.26",
                        "value_Check": False
                    }
                },
            "\\question.json":
                {
                    "Body": [
                        {
                            "Qst": {
                                "question_name": "Кто такой Патрин?",
                                "answer": ["Бугалтер", "Директор"],
                                "right_answer": ["Преподаватель"],
                                "id": 1
                            }
                        }
                    ]
                },
            "\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json":
                {
                    "client_flag": True,
                    "Body": [
                        {
                            "Qst": {
                                "question_name": "Кто такой Патрин?",
                                "answer": ["Бухгалтер ", "Директор"],
                                "right_answer": ["Преподаватель"],
                                "id": 1
                            }
                        }
                    ]
                },
            "\\Settings\\SettingsPage\\settings_page.json":
                {
                    "Body":
                        [
                            {
                                "name": "version",
                                "value": 2.4
                            },
                            {
                                "name": "url for update",
                                "value": "https://github.com/RustFarmer/Test/blob/main/update_url_file.json"
                            }
                        ]

                },
            "\\Settings\\UpdateProgram\\UpdateData\\update_url_file.json":
                {
                    "Body": {
                        "rarFile": "https://github.com/RustFarmer/Rust-helper/raw/refs/heads/main/v5.1.rar"
                    }
                },
            "\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\settings.json":
                {
                    "client_flag": True,
                    "Body": []
                },
            "\\PassCutOff\\settings.json":
                {
                    "Body": []
                },
            "\\ImageResultScreen\\imageSettings.json":
                {
                    "Body": []
                },
            "\\ListBlancQuestion\\listBlancQuestion.json":
                {
                    "Body": []
                }
        }

        logger.info(self.file_path_admin)
        logger.info(self.client_path)
        logger.info(self.filename_list_dict)

    def create_json_file(self):
        logger.info(type(get_absolute_path()))
        logger.info(get_absolute_path())

        logger.info(self.filename_list_dict)

        for key, value in self.filename_list_dict.items():
            filepath = f'{self.file_path_admin}{key}'
            logger.info(filepath)
            try:
                if value.get("client_flag"):
                    filepath = f'{self.client_path}{key}'
                    logger.info(filepath)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            logger.info(key)
                            logger.info(value)
                    except FileNotFoundError:
                        filepath = f'{get_client_path(False)}{key}'
                        with open(filepath, 'r', encoding='utf-8') as f:
                            logger.info(key)
                            logger.info(value)
            except KeyError as e:
                logger.error(e)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    logger.info(key)
                    logger.info(value)
            except FileNotFoundError as e:
                logger.critical(e)
                with open(filepath, 'w', encoding='utf-8') as f:
                    logger.error(key)
                    logger.error(value)
                    json.dump(value.get("Body"), f, ensure_ascii=False, indent=4)
