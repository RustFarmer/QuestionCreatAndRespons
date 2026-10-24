import requests
from loguru import logger

URL_DOWNLOAD_FILE = (
    "https://github.com/RustFarmer/Test/blob/main/url_dowload_file.json"
    .replace("github.com", "raw.githubusercontent.com")
    .replace("/blob/", "/")
)


def get_url_question_list(list_id: int | str) -> str | None:
    """
    Получает ссылку для скачивания списка вопросов по его list_id.

    :param list_id: Идентификатор списка (например, 1, 2, 3 …)
    :return: Ссылка для скачивания или None, если ссылка не найдена / произошла ошибка.
    """
    try:
        response = requests.get(URL_DOWNLOAD_FILE, timeout=10)
        response.raise_for_status()
        data: dict = response.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(e)
        return None

    link = data.get(str(list_id))
    if not link:
        logger.error(f"В url_dowload_file.json нет ключа для list_id={list_id}")
        return None

    return link

