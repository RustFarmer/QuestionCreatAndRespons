# -*- coding: utf-8 -*-
import os
import random
import json
import webview

from pathlib import Path

from flask import Flask, render_template, request
from dataclasses import dataclass

from _check_ import CheckResponse
from _load_percent_ import Percent

from __admin_module__ import get_absolute_path

path = get_absolute_path()
app = Flask(__name__)
filename = f'{path}\\static\\GetClientData\\UploadInServerClientCookie\\ClientCookieData\\question.json'
filename_settings = f'{path}\\static\\exe\\getClientCookie\\password.txt'
file_name_path_no_again = f'{path}\\NoAgain.txt'


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
    d = []
    for item in items:
        qst = item['Qst']
        all_options = qst['answer'] + qst['right_answer']
        random.shuffle(all_options)
        qst['answer'] = all_options
        d = qst['answer']

    return render_template(HtmlPageName.index, items=items, answer=d)


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
    folder_path = Path(f'{path}\\static\\images\\')
    file_list = [item.name for item in folder_path.iterdir()]
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
            return render_template(HtmlPageName.lockWin)
    else:
        with open(file_name_path_no_again, 'w', encoding='utf-8') as f:
            f.writelines("No no no mister fish you no go too save answer")
        if Percent().get_percent(counter, count_true) >= 60:
            return render_template(HtmlPageName.check_result, count_true=count_true,
                                   resultImage=image, count_question=count_question,
                                   result_text="Молодец")
        return render_template(HtmlPageName.check_result, count_true=count_true,
                               resultImage=image, count_question=count_question)


def get_password():
    with open(filename_settings, 'r', encoding='utf-8') as f:
        password = f.readline()
    return password


@app.route("/exitProgram")
def close_program() -> None:
    return windows.destroy()

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    url = f"http://{host}:{port}"
    
    windows = webview.create_window('Admin', app, fullscreen=True)
    webview.start()
    