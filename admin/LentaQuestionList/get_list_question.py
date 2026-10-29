import os
import json
import requests
from loguru import logger
from urllib.parse import urlencode

from fileModule import QuestionListPath
from Settings.JsonKey import download_url_key


def _extract_url_from_data(data):
    """Извлекает URL из строки или словаря."""
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in (download_url_key, "url", "public_key", "link", "href"):
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def _get_public_link(url) -> str | None:
    """Достаёт публичную ссылку Яндекс.Диска из JSON-конфига."""
    if not isinstance(url, str):
        logger.error(f"_get_public_link ожидал str, получил {type(url).__name__}: {url!r}")
        return None

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.exception(e)
        return None

    try:
        data = response.json()
    except ValueError:
        logger.error(
            f"Ответ по {url} — не JSON. "
            f"Content-Type={response.headers.get('Content-Type')!r}, "
            f"начало: {response.text[:200]!r}"
        )
        return None

    link = _extract_url_from_data(data)
    if not link:
        logger.error(f"Не удалось извлечь ссылку из ответа: {data!r}")
    return link


def _decode_questions(content: bytes):
    """Декодирует ответ Яндекс.Диска в список вопросов."""
    if not content:
        return None
    try:
        data = json.loads(content)
    except (ValueError, TypeError) as e:
        logger.exception(e)
        return None

    if not isinstance(data, list):
        logger.error(f"Ожидался JSON-массив, получен {type(data).__name__}")
        return None

    return data


def get_list_question(save_flag=1, url=QuestionListPath.download_url_file, public_links=None):
    """
    Загружает список вопросов.

    :param save_flag: 1 — сохранить в файл; 0/False — вернуть список Python.
    :param url: при save_flag=True — JSON-конфиг с ключом download_url;
                при save_flag=False — публичная ссылка Яндекс.Диска.
    :param public_links: альтернативная публичная ссылка.
    :return: список вопросов при save_flag=False, иначе None.
    """
    logger.info(
        f"[get_list_question] save_flag={save_flag}, "
        f"url={url!r} ({type(url).__name__}), "
        f"public_links={public_links!r} ({type(public_links).__name__})"
    )

    if save_flag:
        public_link = _get_public_link(url)
    else:
        candidate = public_links if public_links else url

        if not candidate:
            logger.error("Не задана публичная ссылка")
            return None

        if isinstance(candidate, dict):
            extracted = _extract_url_from_data(candidate)
            if not extracted:
                logger.error(f"Не удалось извлечь ссылку из словаря: {candidate!r}")
                return None
            candidate = extracted
        elif not isinstance(candidate, str):
            candidate = str(candidate)

        if candidate.startswith("https://disk.yandex.ru/"):
            public_link = candidate
        else:
            public_link = _get_public_link(candidate)

    if not public_link:
        logger.error("Не удалось получить ссылку на файл вопросов")
        return None

    try:
        api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
        response = requests.get(api_url, params={"public_key": public_link}, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as e:
        logger.exception(e)
        return None

    if not isinstance(payload, dict):
        logger.error(f"cloud-api вернул не объект: {type(payload).__name__}: {payload!r}")
        return None

    download_url = payload.get("href")
    if not download_url:
        logger.error(f"В ответе cloud-api нет 'href'. Ответ: {payload!r}")
        return None

    try:
        download_response = requests.get(download_url, timeout=30)
        download_response.raise_for_status()
    except requests.RequestException as e:
        logger.exception(e)
        return None

    if save_flag:
        try:
            os.makedirs(
                os.path.dirname(QuestionListPath.for_write_file_path_and_filename),
                exist_ok=True
            )
            with open(QuestionListPath.for_write_file_path_and_filename, "wb") as f:
                f.write(download_response.content)
            logger.info(
                f"Список вопросов сохранён: "
                f"{QuestionListPath.for_write_file_path_and_filename}"
            )
        except OSError as e:
            logger.exception(e)
        return None

    return _decode_questions(download_response.content)