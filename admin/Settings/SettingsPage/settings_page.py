# -*- coding: utf-8 -*-
import json
from Settings.module import file_path_settings_page as setting_filename


class SettingsPage:
    def __init__(self):
        self.setting_filename = setting_filename

    def load_settings(self) -> list | FileNotFoundError:
        try:
            with open(self.setting_filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError as e:
            return e
