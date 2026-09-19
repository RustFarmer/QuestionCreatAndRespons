import json

from fileModule import FileNameAdmin, FileNameClient


class PassCutOff:
    def __init__(self, filename_settings=FileNameAdmin.filename_settings,
                 filename_image=FileNameAdmin.filename_image_settings,
                 filename_settings_client=FileNameClient.filename_CLINET_settings):
        self.filename_settings_client = filename_settings_client
        self.update_ = None
        self.ResultScreenClient: dict = None
        self.filename_settings: str = filename_settings
        self.filename_image: str = filename_image

    def result_screen_client_dict(self, percent: int, image: str) -> dict:
        self.ResultScreenClient = \
            {
                "ResultScreenClient": {
                    "percent": percent,
                    "image": image
                }
            }
        return self.ResultScreenClient

    def __load_image_data__(self) -> json.load:
        with open(self.filename_image, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def __load_result_screen_dict__(self) -> dict:
        with open(self.filename_settings, 'r', encoding='utf-8') as f:
            self.load_result_screen_dict = json.load(f)
        return self.load_result_screen_dict

    def __settings_file_pass_cut_off_dict(self) -> dict:
        self.settings_file_pass_cut_off_dict = {
            "ResultScreenClient": []
        }
        return self.settings_file_pass_cut_off_dict

    def __save_pass_cut_off__(self, percent: int, image: str, flag=0) -> bool:
        try:
            with open(self.filename_settings, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data.append(self.result_screen_client_dict(percent, image))
            data.sort(key=lambda x: x['ResultScreenClient']['percent'])

            with open(self.filename_settings, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            with open(self.filename_settings_client, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True

        except FileNotFoundError as e:
            if flag == 0:
                return e
            print(f"Error: {e}")
            with open(self.filename_settings, 'w', encoding='utf-8'):
                ...
            print(f"File create")
            if self.__save_pass_cut_off__(percent, image, flag=1):
                return True
            return False

    def __clear_file_pass_cut_off__(self):
        data = []
        with open(self.filename_settings, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        with open(self.filename_settings_client, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
