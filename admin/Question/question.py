# -*- coding: utf-8 -*-
import json
from loguru import logger
from firstRun import get_client_path, get_absolute_path
from fileModule import FileNameAdmin, FileNameClient

file_path_admin = get_absolute_path()
file_path_client = get_client_path()


class Question:
    def __init__(self, question_id=1):
        self.question_dict = None
        self.filename_CLIENT = FileNameClient.filename_CLINET_question
        self.filename = FileNameAdmin.filename_question
        self.right_answer = None
        self.answer = None
        self.name = None
        if question_id == 1:
            self.id = question_id
            self.check_id_in_input_question()
        else:
            self.id = self.qs_id()

    def question_dicts(self) -> dict:
        self.question_dict = {
            "Qst": {
                "question_name": self.name,
                "answer": self.answer,
                "right_answer": self.right_answer,
                "id": self.id
            }
        }
        return self.question_dict

    def check_id_in_input_question(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for x in data:
            if x['Qst']['id'] == self.id:
                self.id = self.qs_id()
        return self.id

    def save_question(self, name: str, answer: list[str],
                      right_answer: list[str] | str):
        self.right_answer = right_answer
        self.answer = answer
        self.name = name
        self.question_dict = self.question_dicts()

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(data)
            data = list(data) + [self.question_dict]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            with open(self.filename_CLIENT, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def delete_qst(self, qst_id):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            new_data = [u for u in data if u['Qst']['id'] != qst_id]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
            with open(self.filename_CLIENT, 'r', encoding='utf-8') as f:
                data = json.load(f)
            new_data = [u for u in data if u['Qst']['id'] != qst_id]
            with open(self.filename_CLIENT, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def qs_id(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(data)
        if not data:
            last_id = 0
        else:
            last_items = data[-1]
            last_id = last_items["Qst"]["id"]
        self.id = last_id + 1
        return self.id


class QuestionList:
    def __init__(self, filename='../admin/ListBlancQuestion/listBlancQuestion.json'):
        self.show_name = None
        self.save_file_dict = None
        self.question = None
        self.question_id = None
        self.question_dict = None
        self.filename = filename
        self.list_name = None
        self.list_id = None
        self.question_list_dict = self.question_dicts()
        self.list_filename = None

    def question_dicts(self) -> dict:
        self.question_list_dict = {
            "Qst_list": {
                "list_name": self.qs_id(),
                "show_name": self.show_name,
                "question_id": self.question_id,
                "id": self.list_id
            }
        }
        return self.question_list_dict

    def qs_id(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not data:
            last_id = 0
        else:
            last_items = data[-1]
            last_id = last_items["Qst_list"]["id"]
        self.list_id = last_id + 1
        return self.list_id

    def save_in_list(self, name, question_id, question_dict):
        self.question_id = question_id
        self.show_name = name
        self.list_name = self.qs_id()
        self.question = question_dict
        self.question_dict = self.question_dicts()
        self.list_filename = f'../admin/ListBlancQuestion/overListQuestion/{self.list_name}.json'

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data = list(data) + [self.question_dict]

            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            with open(self.list_filename, 'w', encoding='utf-8') as f:
                json.dump(question_dict, f, indent=4, ensure_ascii=False)

        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def delete_qst(self, qst_id):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            new_data = [u for u in data if u['Qst_list']['id'] != qst_id]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=4, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


class ChangeQuestionList:
    def __init__(self):
        self.filename_CLIENT = FileNameClient.filename_CLINET_question
        self.filename = FileNameAdmin.filename_question

    def update_question_list(self, file):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(file, f, indent=4, ensure_ascii=False)

        with open(self.filename_CLIENT, 'w', encoding='utf-8') as f:
            json.dump(file, f, indent=4, ensure_ascii=False)


class ChangeQuestion:
    def __init__(self, question_id):
        self.filename = FileNameAdmin.filename_question
        self.filename_client = FileNameClient.filename_CLINET_question
        self.id = question_id
        self.right_answer = None
        self.answer = None
        self.name = None

    def question_dicts(self) -> dict:
        return {
            "Qst": {
                "question_name": self.name,
                "answer": self.answer,
                "right_answer": self.right_answer,
                "id": self.id
            }
        }

    def update_question(self, file):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(file, f, indent=4, ensure_ascii=False)

        with open(self.filename_client, 'w', encoding='utf-8') as f:
            json.dump(file, f, indent=4, ensure_ascii=False)

    def save_question(self, name: str, answer: list[str], right_answer: list[str]):
        self.right_answer = right_answer
        self.answer = answer
        self.name = name

        new_question = self.question_dicts()
        logger.info(new_question)

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        new_id = new_question['Qst']['id']

        index_to_replace = None
        logger.info(data)
        for i, item in enumerate(data):

            logger.info(i)
            logger.info(item)
            logger.info(repr(enumerate(data)))

            if item.get('Qst', {}).get('id') == new_id:
                index_to_replace = i
                break

        logger.info(index_to_replace)

        if index_to_replace is not None:
            data[index_to_replace] = new_question
            logger.info(f"Вопрос с id {new_id} обновлён")
        else:
            data.append(new_question)
            logger.info(f"Добавлен новый вопрос с id {new_id}")

        data.sort(key=lambda x: x['Qst']['id'])

        logger.info(data)

        self.update_question(data)


class ChangeQuestionID:
    def __init__(self):
        self.filename = FileNameAdmin.filename_question
        self.data = self.__load_file__()

    def __load_file__(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(data)
            return data
        except FileNotFoundError as e:
            print(e)
            return e

    def change_id(self):
        counter = 0

        for x in self.data:
            counter += 1
            item = x['Qst']

            question_name = item['question_name']

            answer = item['answer']

            right_answer = item['right_answer']

            qst_id = item['id']

            Question().delete_qst(qst_id)
            Question().save_question(question_name, answer, right_answer)
