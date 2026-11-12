import json
from Settings.module import file_path_new_version_info_data

def get_whats_new_dismiss() -> dict:
    try:
        print(file_path_new_version_info_data, "p927j3-50qj2374=0fc5q239740")
        with open(file_path_new_version_info_data, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        return e