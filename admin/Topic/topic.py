import json
from loguru import logger
from Topic.module import File_path

class Topic:
    def __init__(self, filename_save=None, topic_settings_data=None):
        self.filename_settings = File_path.topic_settings
        print(self.filename_settings)
        self.filename_save = File_path.topic_save
        self.topic_save_data = self.load(self.filename_save)
        self.topic_settings_data = self.load(self.filename_settings)
        self.append_topic = []
        
        self._topic_key: str = "Topic"
        self._topic_name_key: str = "topic_name"
        self._topic_id_key: str = "topic_id"
        self._topic_py_file_name_html_name_key: str = "py_file_name_html_name"
        self._topic_style_key = "topic_style"
        
    def load(self, filename) -> list | Exception:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                topic_settings_data = json.load(f)
                
            logger.info(topic_settings_data)
            return topic_settings_data
                
        except FileNotFoundError as e:
            logger.error(e)
            return e

class GetTopic(Topic):
    def __init__(self, topic_id, filename_save=None, topic_settings_data=None):
        super().__init__(filename_save, topic_settings_data)
        self._topic: dict = dict(*[x for x in self.topic_save_data if x[self._topic_key][self._topic_id_key] == topic_id])
        self._for_topic: dict = dict(*[x for x in self.topic_settings_data])

    def get_topic(self) -> dict:
        return self._for_topic
    
    def get_topic_file(self) -> str:
        return str(self._for_topic[self._topic_key][self._topic_py_file_name_html_name_key])

    def get_topic_name(self) -> dict:
        return self._for_topic.get(self._topic_name_key)

    def get_topic_name_for_id(self) -> dict:
        return self._topic[self._topic_key][self._topic_id_key]
    
    def get_topic_for_id(self):
        return self._topic

    def get_py_file_name_html_name_for_id(self) -> dict:
        return self._topic[self._topic_key][self._topic_py_file_name_html_name_key]
    
    def get_last_topic_id(self) -> int | None:
        if not self.topic_save_data:
            return None
        return max(
            item[self._topic_key][self._topic_id_key]
            for item in self.topic_save_data
        )
        
class ChangeTopic(Topic):
    def __init__(self, filename_save=None, topic_settings_data=None):
        super().__init__(filename_save, topic_settings_data)
    
    def change_topic(self) -> int | Exception:
        try:
            with open(self.filename_settings, 'r', encoding='utf-8') as f:
                data: list = json.load(f)
            _data: dict = dict(*data)
            topic_id = _data[self._topic_key][self._topic_id_key]
            
            __topic = GetTopic(topic_id).get_topic_for_id()
            
            _next_topic = [GetTopic(topic_id=topic_id + 1).get_topic_for_id()]

            if _next_topic == [{}]:
                _next_topic = [GetTopic(topic_id=1).get_topic_for_id()]
            
            logger.info(__topic)
            logger.info(_next_topic)
            
            with open(self.filename_settings, 'w', encoding='utf-8') as f:
                json.dump(_next_topic, f, ensure_ascii=False, indent=4)
            
            return topic_id   
        except Exception as e:
            logger.exception(e)
            return e
    
    def change_for_certain(self, topic_id: int):
        if self.change_topic() == topic_id:
            return True
        return self.change_for_certain(topic_id)

class CreateTopic(Topic):
    def __init__(self, filename_save=None, topic_settings_data=None):
        super().__init__(filename_save, topic_settings_data)
        self.topic_id = self._topic_id()
        
    def create_topic(self, topic_name: str, topic_py_file_name: str, topic_style: str):
        topic_dict: dict = {
            "Topic": {
                "topic_name": topic_name,
                "topic_style": topic_style,
                "py_file_name_html_name": 
                        topic_py_file_name,
                "topic_id": self.topic_id
            }
        }
        
        self.topic_save_data.append(topic_dict)
        
        try:
            with open(self.filename_save, 'w', encoding='utf-8') as f:
                json.dump(self.topic_save_data, f, ensure_ascii=False, indent=4)
        
            logger.info(topic_dict)
            return True
        
        except FileNotFoundError as e:
            logger.error(e)
            return e
        
    def _topic_id(self):
        ids = []
        for item in self.topic_save_data:
            if isinstance(item, dict):
                tid = item.get(self._topic_key, {}).get(self._topic_id_key)
                if isinstance(tid, int):
                    ids.append(tid)
        return max(ids, default=0) + 1

class SaveTopic(Topic):
    def __init__(self, filename_save=None, topic_settings_data=None):
        super().__init__(filename_save, topic_settings_data)
    
    def save_topic(self, topic_dict_for_save: dict) -> bool | FileNotFoundError:
        try:
            with open(File_path.topic_save, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data = list(data) + [topic_dict_for_save]
            
            logger.info(data)
            
            with open(File_path.topic_save, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            logger.error(e)
            return e
        
class DownloadTopic(Topic):
    def __init__(self, filename_save=None, topic_settings_data=None):
        super().__init__(filename_save, topic_settings_data)
        
    def download_topic(self, topic_id: int, all_topic: dict) -> bool:
        topic_dict_for_save = dict(*[x for x in all_topic if x[self._topic_key][self._topic_id_key] == topic_id])
        
        topic_name = topic_dict_for_save[self._topic_key][self._topic_name_key]
        topic_py_file_name_html_name = topic_dict_for_save[self._topic_key][self._topic_py_file_name_html_name_key]
        topic_style = topic_dict_for_save[self._topic_key][self._topic_style_key]
        
        logger.info(topic_name)
        logger.info(topic_py_file_name_html_name)
        logger.info(topic_style)
        
        CreateTopic().create_topic(topic_name=topic_name, topic_py_file_name=topic_py_file_name_html_name, topic_style=topic_style)
        top_id_new_save = GetTopic(1).get_last_topic_id()
        
        logger.info(top_id_new_save)
        return top_id_new_save
        