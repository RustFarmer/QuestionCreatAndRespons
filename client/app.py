# -*- coding: utf-8 -*-
import os
import random
import json
# import webview

from pathlib import Path

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from dataclasses import dataclass

from _check_ import CheckResponse
from _load_percent_ import Percent

from __admin_module__ import get_absolute_path

path = get_absolute_path()
app = Flask(__name__)
filename = f'{path}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json'
filename_settings = f'{path}\\static\\exe\\getClientCookie\\password.txt'
file_name_path_no_again = f'{path}\\NoAgain.txt'


def get_password():
    with open(filename_settings, 'r', encoding='utf-8') as f:
        pas = f.readline()
    return pas


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

        answers = qst.get('answer') or []
        rights = qst.get('right_answer') or []
        if not isinstance(answers, list):
            answers = [answers]
        if not isinstance(rights, list):
            rights = [rights]

        all_options = list(answers) + list(rights)
        random.shuffle(all_options)
        qst['answer'] = all_options

    return render_template(HtmlPageName.index, items=items)


@app.route('/save/all_answer', methods=['POST'])
def save_all_answer():
    counter = 0
    print(request.form.to_dict().get("password"))
    print(request.form.to_dict().get("password") is None)
    answers = request.form.to_dict()
    print(answers)
    parsed = {}
    for key, value in answers.items():
        if key.startswith('answer_'):
            q_id = key.split('_', 1)[1]
            parsed[q_id] = value
            counter += 1
    count_true = CheckResponse().check(parsed)
    folder_path = Path(f'{path}\\static\\images\\')
    image = Percent().check_result(counter, count_true)
    count_question = counter

    if os.path.exists(file_name_path_no_again):
        request_password = request.form.get('password', '')
        true_password = get_password()
        if request_password == true_password:
            os.remove(file_name_path_no_again)
            if Percent().get_percent(counter, count_true) >= 60:
                return render_template(HtmlPageName.check_result, count_true=count_true,
                                       resultImage=image, count_question=count_question,
                                       result_text="Молодец")
            return render_template(HtmlPageName.check_result, count_true=count_true,
                                   resultImage=image, count_question=count_question)
        else:
            return render_template(HtmlPageName.lockWin, parsed=parsed)
    else:
        with open(file_name_path_no_again, 'w', encoding='utf-8') as f:
            f.writelines("No no no mister fish you no go too save answer")
        if Percent().get_percent(counter, count_true) >= 60:
            return render_template(HtmlPageName.check_result, count_true=count_true,
                                   resultImage=image, count_question=count_question,
                                   result_text="Молодец")
        return render_template(HtmlPageName.check_result, count_true=count_true,
                               resultImage=image, count_question=count_question)


@app.route("/exitProgram")
def close_program() -> None:
    return windows.destroy()


@app.route('/check_password', methods=['POST'])
def check_password():
    request_password = request.form.get('password', '').strip()
    true_password = get_password().strip()
    if request_password == true_password:
        if os.path.exists(file_name_path_no_again):
            os.remove(file_name_path_no_again)
        return redirect(url_for('index'))
    return render_template(HtmlPageName.lockWin, error="Неверный пароль")


if __name__ == "__main__":
    print("olihsrgo")
    host = "127.0.0.1"
    port = 5000
    url = f"http://{host}:{port}"

    # windows = webview.create_window('Cient', app, fullscreen=True)
    # webview.start()
    app.run(debug=True)
