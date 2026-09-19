import json
from __admin_module__ import get_absolute_path

path = get_absolute_path()
filename = f'{path}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json'


class Percent:
    def __init__(self,
                 settings_filename=f'{path}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\settings.json'):
        self.filename = settings_filename

    def __load_dict__(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError as e:
            return False, print(e)

    @staticmethod
    def get_percent(count_question, count_write_question):
        if count_write_question == 0:
            return 0
        return (count_write_question / count_question) * 100

    def check_result(self, count_question, count_write_question):
        data = self.__load_dict__()
        percent = self.get_percent(count_question, count_write_question)

        if not data:
            return "aabd7352e02bd43b001fdf142709c294.jpg"

        results = [(item["ResultScreenClient"]["percent"], item["ResultScreenClient"]["image"]) for item in data]
        results.sort(key=lambda x: x[0])

        if percent < results[0][0]:
            return results[0][1]

        for i in range(len(results) - 1):
            if results[i][0] <= percent < results[i + 1][0]:
                return results[i][1]

        return results[-1][1]
