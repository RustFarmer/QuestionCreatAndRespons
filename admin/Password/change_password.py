from Password.get_password import GetPassword
from Password.set_password import SetPassword


class ChangePassword:
    def __init__(self):
        pass

    @staticmethod
    def change_password(file_path_admin, file_path_loger, file_name_log, file_path_client, password):
        if GetPassword().get_password(file_path_admin) is not True:
            SetPassword(file_path_admin, file_path_loger, file_name_log, file_path_client=file_path_client).set_password(password)
            return True
        return False
