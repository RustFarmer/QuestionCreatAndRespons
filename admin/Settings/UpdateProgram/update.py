# -*- coding: utf-8 -*-
from Settings.UpdateProgram.CheckInternetConnection.InterconnectionCheck import InterconnectionCheck
from Settings.UpdateProgram.CheckVersion.CheckVersionProgram import CheckVersionProgram
from Settings.UpdateProgram.DownloadProgram.downloardProgramm import download
from Settings.UpdateProgram.SaveUrlFile.save_url_file import SaveUrlFile


class Update:
    def __init__(self, file_data_url: str | None = None):
        self.file_data_url = file_data_url

    def all_check(self) -> bool:
        if InterconnectionCheck().__check_connection_in_git_hub__():
            if CheckVersionProgram().__check_version__():
                return True
        return False

    def run(self, file_data_url: str | None = None) -> None:
        url = file_data_url or self.file_data_url
        if not url:
            raise ValueError("file_data_url не задан ни в __init__, ни в run()")

        if self.all_check():
            SaveUrlFile(url).save_url_file()
            download()