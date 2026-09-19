from firstRun import get_client_path, get_absolute_path

file_path_admin = get_absolute_path()
file_path_client = get_client_path()

UPLOAD_FOLDER = f'{file_path_admin}\\ImageResultScreen\\Image'
UPLOAD_FOLDER_CLIENT = f'{file_path_client}\\static\\images\\'

filename_cookie: str = f'{file_path_admin}\\Cookie\\local_cookie.json'


class FilePathLogApp:
    file_path_app = f'{file_path_admin}\\Log'
    file_path_settings = f'{file_path_admin}\\Log'


class FileNameAdmin:
    filename_question = f'{file_path_admin}\\question.json'

    filename_list = f'{file_path_admin}\\ListBlancQuestion\\listBlancQuestion.json'

    filename_change_file = f'{file_path_admin}\\ListBlancQuestion\\overListQuestion\\'

    filename_image_settings = f'{file_path_admin}\\ImageResultScreen\\imageSettings.json'

    filename_settings = f'{file_path_admin}\\PassCutOff\\settings.json'

    image_path = f'{file_path_admin}\\ImageResultScreen\\Image'

    filename_password = f'{file_path_admin}\\Password'


class FileNameClient:
    filename_CLINET_settings = f"{file_path_client}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\settings.json"
    filename_CLINET_question = f"{file_path_client}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json"
    # filename_CLINET_image_settings = f"{file_path_client}\static\GetClientData\\UploadInServerClientCookie\ClientCookieData\ImageSettings.json"
    filename_CLINET_image_settings = f"{file_path_client}\\static\\images"
    image_path_CLIENT = f'{file_path_client}\\static\\images\\'
    filename_CLIENT_password = f'{file_path_client}\\static\\exe\\getClientCookie'
