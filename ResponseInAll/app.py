# -*- coding: utf-8 -*-
import random
import json
import webview


from flask import Flask, render_template, request, send_from_directory, jsonify
from dataclasses import dataclass

from _check_ import CheckResponse
from _load_percent_ import Percent

from __admin_module__ import get_absolute_path

path = get_absolute_path()
app = Flask(__name__)
filename = f'{path}\\question.json'


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_folder = str(path / 'static' / 'images')
    return send_from_directory(upload_folder, filename)


@dataclass()
class HtmlPageName:
    index = 'index.html'
    check_result = 'result.html'
    lockWin = 'lockWindows.html'


def load_items():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    except (FileNotFoundError, json.JSONDecodeError):
        with open('../admin/question.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    return data


@app.route('/')
def index():
    items = load_items()

    for item in items:
        qst = item['Qst']
        if qst['id'] == 1:
            answers = qst.get('answer') or []
            rights = qst.get('right_answer') or []

            if not isinstance(answers, list):
                answers = [answers]
            if not isinstance(rights, list):
                rights = [rights]

            all_options = list(answers) + list(rights)
            random.shuffle(all_options)
            qst['answer'] = all_options

            return render_template(HtmlPageName.index, items=[item])

    return render_template(HtmlPageName.index, items=[])


@app.route('/save/all_answer', methods=['POST'])
def save_all_answer():
    counter = 0
    answers = request.form.to_dict()
    parsed = {}
    for key, value in answers.items():
        if key.startswith('answer_'):
            q_id = key.split('_', 1)[1]
            parsed[q_id] = value
            counter += 1
    count_true = CheckResponse().check(parsed)

    image = Percent().check_result(counter, count_true)
    count_question = counter

    if count_true == 1:
        return jsonify({"result": True})
    return jsonify({"result": False})


@app.route("/exitProgram")
def close_program() -> None:
    return windows.destroy()


@app.route("/next/<int:question_id>")
def next_question(question_id):
    question_id += 1
    items = load_items()
    for item in items:
        qst = item['Qst']
        if qst['id'] == question_id:
            answers = qst.get('answer') or []
            rights = qst.get('right_answer') or []

            if not isinstance(answers, list):
                answers = [answers]
            if not isinstance(rights, list):
                rights = [rights]

            all_options = list(answers) + list(rights)
            random.shuffle(all_options)
            qst['answer'] = all_options

            return render_template(HtmlPageName.index, items=[item])

    return jsonify({"No question": True})


@app.route("/last/<int:question_id>")
def last_question(question_id):
    question_id -= 1
    if question_id <= 1:
        return index()
    items = load_items()
    for item in items:
        qst = item['Qst']
        if qst['id'] == question_id:
            answers = qst.get('answer') or []
            rights = qst.get('right_answer') or []

            if not isinstance(answers, list):
                answers = [answers]
            if not isinstance(rights, list):
                rights = [rights]

            all_options = list(answers) + list(rights)
            random.shuffle(all_options)
            qst['answer'] = all_options

            return render_template(HtmlPageName.index, items=[item])


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    url = f"http://{host}:{port}"
    # app.run(debug=True)
    windows = webview.create_window('ResponseInAll', app, fullscreen=True)
    webview.start()
