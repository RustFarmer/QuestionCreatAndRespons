# -*- coding: utf-8 -*-

from Settings.UpdateProgram.CheckInternetConnection.InterconnectionCheck import InterconnectionCheck
from Settings.UpdateProgram.CheckVersion.CheckVersionProgram import CheckVersionProgram
from Settings.UpdateProgram.DownloadProgram.downloardProgramm import download


class Update:
    def __init__(self):
        pass

    def all_check(self):
        if InterconnectionCheck().__check_connection_in_git_hub__():
            if CheckVersionProgram().__check_version__():
                return True
        return False

    # def update_cookie(self):

    def run(self):
        if self.all_check():
            # Сначала обновляем локальный файл с URL
            SaveUrlFile().save_url_file()
            # Затем открываем браузер с новым URL
            download()
