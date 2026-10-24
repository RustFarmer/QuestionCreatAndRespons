import json
from fileModule import QuestionListPath


def load_question_list() -> json.JSONDecoder | FileNotFoundError:
    try:
        with open(QuestionListPath.for_write_file_path_and_filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        return e
