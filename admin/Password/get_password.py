from pathlib import Path


class GetPassword:
    def __init__(self):
        self.filename = 'password.txt'
        self.password = None

    def get_password(self, file_path: Path) -> str | FileNotFoundError:
        try:
            with open(f'{file_path}\\{self.filename}', 'r', encoding='utf-8') as f:
                self.password = f.readline()
            return str(self.password)
        except FileNotFoundError as e:
            return e
