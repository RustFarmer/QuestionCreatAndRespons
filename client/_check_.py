import json
import os
from __admin_module__ import get_absolute_path

path = get_absolute_path()
filename = f'{path}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json'


def _answer_key(ans):
    if isinstance(ans, dict):
        return ans.get('text') or ans.get('image') or ''
    return ans


class CheckResponse:
    def __init__(self,
         filename=f'{path}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json'):
        self.filename = filename

    def check(self, answer):
        count_true = 0
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            backup = f'{path.parent}\\admin\\question.json'
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                os.makedirs(os.path.dirname(self.filename), exist_ok=True)
                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

        questions = {item['Qst']['id']: item['Qst'] for item in data}

        for qid, user_ans in answer.items():
            qid = int(qid)
            if qid not in questions:
                continue
            q = questions[qid]

            right_ans = q.get('right_answer') or []
            if not isinstance(right_ans, list):
                right_ans = [right_ans]

            if not isinstance(user_ans, list):
                user_ans = [user_ans]

            right_keys = {_answer_key(a) for a in right_ans}
            user_keys = {_answer_key(a) for a in user_ans}

            if right_keys & user_keys:
                count_true += 1

        return count_true
