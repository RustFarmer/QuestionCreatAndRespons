import json
from fileModule import QuestionListPath


def load_question_list(filename: str=QuestionListPath.for_write_file_path_and_filename) -> json.JSONDecoder | FileNotFoundError:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        return e
