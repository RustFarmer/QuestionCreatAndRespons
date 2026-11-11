import requests
from loguru import logger

from fileModule import QuestionListPath
from Settings.JsonKey import download_url_key


def create_url_for_download(url: str) -> str:
    return (
        url
        .replace("github.com", "raw.githubusercontent.com")
        .replace("/blob/", "/")
    )


def get_list_question(url=QuestionListPath.download_url_file, public_links=None) -> list[dict]:
    """
    Загружает список вопросов и возвращает распарсенный JSON (list[dict]),
    либо None при ошибке.
    """
    logger.info(
        f"url={url!r} ({type(url).__name__}), "
    )

    try:
        response = requests.get(create_url_for_download(url), timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(e)
        return None

    logger.info(data)
    return data