import requests
from loguru import logger

main_url = "https://github.com/RustFarmer/Test/blob/main/I_m_tired.json"
dd = "https://raw.githubusercontent.com/RustFarmer/Test/refs/heads/main/topic_save.json"

def create_url_for_download(url: str) -> str:
    return (
        url
        .replace("github.com", "raw.githubusercontent.com")
        .replace("/blob/", "/")
    )


def get_topic(topic_id: int) -> str:
    topics_response = requests.get(create_url_for_download(main_url))
    topics_response.raise_for_status()
    topics_map: dict = topics_response.json()

    topic_path = topics_map.get(str(topic_id))
    if topic_path is None:
        raise KeyError(f"topic {topic_id} not found; available: {list(topics_map.keys())}")
    logger.info(topic_path)

    topic_url = create_url_for_download(topic_path)
    logger.info(topic_url)

    topic_response = requests.get(topic_url)
    topic_response.raise_for_status()
    return topic_response.text


def get_all_topics():
    all_topics_response = requests.get(dd)
    all_topics_response.raise_for_status()
    return all_topics_response.json()
