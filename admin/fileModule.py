from dataclasses import dataclass
from firstRun import get_client_path, get_client_in_all_path, get_absolute_path

file_path_admin = get_absolute_path()
file_path_client = get_client_path()
file_path_client_all = get_client_in_all_path()

UPLOAD_FOLDER = f'{file_path_admin}/ImageResultScreen/Image'
UPLOAD_FOLDER_CLIENT = f'{file_path_client}/static/images/'

filename_cookie: str = f'{file_path_admin}/Cookie/local_cookie.json'

load_question_list_cookie: str = f"{file_path_admin}/LentaQuestionList/Cookie/local_cookie.json"


@dataclass(frozen=True)
class FilePathLogApp:
    file_path_app = f'{file_path_admin}/Log'
    file_path_settings = f'{file_path_admin}/Log'


@dataclass(frozen=True)
class FileNameAdmin:
    filename_question = f'{file_path_admin}/question.json'

    filename_list = f'{file_path_admin}/ListBlancQuestion/listBlancQuestion.json'

    filename_change_file = f'{file_path_admin}/ListBlancQuestion/overListQuestion/'

    filename_image_settings = f'{file_path_admin}/ImageResultScreen/imageSettings.json'

    filename_settings = f'{file_path_admin}/PassCutOff/settings.json'

    image_path = f'{file_path_admin}/ImageResultScreen/Image'

    filename_password = f'{file_path_admin}/Password'

    fillename_QuestionList = f'{file_path_admin}/ListBlancQuestion/listBlancQuestion.json'

    filename_list_question_file = f'{file_path_admin}/ListBlancQuestion/overListQuestion/'


@dataclass(frozen=True)
class FileNameClient:
    filename_CLINET_settings = f"{file_path_client}/static/GetClientData/UploadInServerClientCookie/ClientCookieData/settings.json"
    filename_CLINET_question = f"{file_path_client}/static/GetClientData/UploadInServerClientCookie/ClientCookieData/question.json"
    # filename_CLINET_image_settings = f"{file_path_client}\static\GetClientData/UploadInServerClientCookie\ClientCookieData\ImageSettings.json"
    filename_CLINET_image_settings = f"{file_path_client}/static/images"
    image_path_CLIENT = f'{file_path_client}/static/images/'
    filename_CLIENT_password = f'{file_path_client}/static/exe/getClientCookie'

    filename_CLIENT_IN_ALL_question = f"{file_path_client_all}/question.json"
    filename_CLIENT_IN_ALL_settings = f"{file_path_client_all}/settings.json"


@dataclass(frozen=True)
class QuestionListPath:
    dir_question_list = f"{file_path_admin}/ListBlancQuestion/overListQuestion"
    save_response_question_list = f"{file_path_admin}/LentaQuestionList/save_dir_response_question_list"
    question_list_filename = "QuestionList.json"
    for_write_file_path_and_filename = f"{save_response_question_list}/{question_list_filename}"
    download_url_file = (
        "https://github.com/RustFarmer/Test/blob/main/download_url_file.json"
        .replace("github.com", "raw.githubusercontent.com")
        .replace("/blob/", "/")
    )
