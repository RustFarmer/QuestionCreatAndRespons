import requests

from Settings.module import git_hab_url

class InterconnectionCheck:
    def __init__(self):
        self.git_hab_url = git_hab_url

    def __check_connection_in_git_hub__(self):
        try:
            response = requests.get(self.git_hab_url)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
