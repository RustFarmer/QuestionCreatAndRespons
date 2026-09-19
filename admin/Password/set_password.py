import os
from loguru import logger


class SetPassword:
    def __init__(self, file_path_admin, file_path_loger, file_name_log, file_path_client):
        logger.add(f"{file_path_loger}\\{file_name_log}",
                   format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

        self.filename_admin = f"{file_path_admin}\\password.txt"
        self.filename_client = f"{file_path_client}\\password.txt"

    def set_password(self, password):
        try:
            with open(self.filename_admin, 'r', encoding='utf-8') as f:
                data = f.readline()
            if data == "":
                with open(self.filename_admin, 'w', encoding='utf-8') as f:
                    f.writelines(password)
                with open(self.filename_client, 'w', encoding='utf-8') as f:
                    f.writelines(password)
                return True
            os.remove(self.filename_admin)
            os.remove(self.filename_client)
            return self.set_password(password)
        except FileNotFoundError as e:
            logger.info(e)
            with open(self.filename_admin, 'w', encoding='utf-8') as f:
                f.writelines(password)
            with open(self.filename_client, 'w', encoding='utf-8') as f:
                f.writelines(password)
                return True
