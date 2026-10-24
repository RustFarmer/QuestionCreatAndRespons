import json


def update_question_list(file_path_and_name, save_data) -> bool | FileNotFoundError:
    try:
        with open(file_path_and_name, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
        return True
    except FileNotFoundError as e:
        return e