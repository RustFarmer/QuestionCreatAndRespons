import ast
from urllib.parse import unquote


def get_parameter_sing_question(url: str) -> dict:
    if '://' in url:
        url = url.split('://', 1)[1]

    parts = [p for p in url.split('/') if p]

    data = {}
    for part in parts:
        if '=' not in part:
            continue
        key, value = part.split('=', 1)
        key = unquote(key)
        value = unquote(value)

        if key == 'right_answer' or key == 'answer':
            try:
                data[key] = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                data[key] = value
        else:
            data[key] = value

    return data
