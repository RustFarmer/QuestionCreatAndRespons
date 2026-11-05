# -*- coding: utf-8 -*-
import os
import shutil
import json
import requests
import webview

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
from loguru import logger

from ShareList.create_url import Url
from ShareList.get_parametr_in_url import get_parameter_sing_question

from Question.question import Question, QuestionList, ChangeQuestion, ChangeQuestionList, ChangeQuestionID
from Question.update_question_list import update_question_list

from ImageResultScreen.save_image import SaveImage
from ImageResultScreen.load_image import LoadImage
from ImageResultScreen.delete_image import DeleteImage

from PassCutOff.pass_cut_off import PassCutOff

from Settings.UpdateProgram.update import Update
from Settings.UpdateProgram.GetFileUrl.getFileUrlForDownload import getFileUrlForDownload
from Settings.UpdateProgram.SaveUrlFile.save_url_file import SaveUrlFile
from Settings.SettingsPage.settings_page import SettingsPage
from Settings.module import file_data_url

from Cookie.local_cookie import update_session
from Password.change_password import ChangePassword

from LentaQuestionList.load_list_question import load_question_list
from LentaQuestionList.get_list_question import get_list_question
from LentaQuestionList.get_file_question_list import get_url_question_list

from Topic.topic import GetTopic, ChangeTopic, DownloadTopic
from Topic.DownloadTopic.download_topic import get_topic, get_all_topics
from firstRun import FirstRun
from fileModule import HtmlPageName, RedirectHtmlPage, FileNameAdmin, FileNameClient, FilePathLogApp, filename_cookie, load_question_list_cookie, QuestionListPath, \
    UPLOAD_FOLDER, UPLOAD_FOLDER_CLIENT, UPLOAD_FOLDER_RESPONSELL_ALL,file_path_admin

logger.add(f"{FilePathLogApp.file_path_app}\\appFileLog.log",
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

logger.info(f"{FilePathLogApp.file_path_app}\\appFileLog.log")
d = 0

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_CLIENT'] = UPLOAD_FOLDER_CLIENT
app.config['UPLOAD_FOLDER_RESPONSELL_ALL'] = UPLOAD_FOLDER_RESPONSELL_ALL

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = os.getenv("oihapgoihopasdfimnposajiSuperSecretCode",
                           "AKRJGFUgfockbucgekdjfbgaljydgfcabsdfojhags--=204913-048=ey")


def save_uploaded_file(file):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_CLIENT'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_RESPONSELL_ALL'], exist_ok=True)
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_path_client = os.path.join(app.config['UPLOAD_FOLDER_CLIENT'], filename)
    file_path_client_all = os.path.join(app.config['UPLOAD_FOLDER_RESPONSELL_ALL'], filename)
    
    file.save(file_path)
    
    shutil.copy2(file_path, file_path_client)
    shutil.copy2(file_path, file_path_client_all)
    
    return filename


def cookie(filename=filename_cookie) -> tuple[Any, str | FileNotFoundError | None]:
    """
    Returns:
        value_check, update_url
    """
    value_check = update_session(filename, file_data_url=file_data_url)
    try:
        if value_check:
            SaveUrlFile(file_data_url).save_url_file()
            update_url = getFileUrlForDownload().get_url
        else:
            update_url = None
    except TimeoutError:
        update_url = None

    logger.info(value_check)
    logger.info(update_url)

    return value_check, update_url


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def items_load(filenames=FileNameAdmin.filename_question):
    try:
        with open(filenames, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        data = []

        with open(filenames, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(filenames, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(FileNameAdmin.filename_list, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(FileNameAdmin.filename_list, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with open(FileNameClient.filename_CLINET_question, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open(FileNameClient.filename_CLINET_question, 'r', encoding='utf-8') as f:
            data = json.load(f)

    return data


def change_items_load(item):
    with open(FileNameAdmin.filename_question, 'w', encoding='utf-8') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)

    with open(FileNameClient.filename_CLINET_question, 'w', encoding='utf-8') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)



@app.route('/')
def index():
    get_style = GetTopic(1).get_topic()
    
    itemss = items_load()
    value_check, update_url = cookie()

    logger.info(itemss)
    topic = GetTopic(1).get_topic()
    logger.info(topic)
    return render_template(HtmlPageName.index, items=itemss, update=value_check, update_url=update_url, style=get_style, current_topic=get_style)


@app.route('/create_question', defaults={'list_id': None}, methods=['GET', 'POST'])
@app.route('/create_question/<int:list_id>', methods=['GET', 'POST'])
def create_question(list_id):
    get_style = GetTopic(1).get_topic()
    
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answers = request.form.getlist('answers[]')
        answers_true = request.form.getlist('answers_true[]')

        question_image = request.files.get('question_image')
        answer_images = request.files.getlist('answer_images[]')
        answer_true_images = request.files.getlist('answer_true_images[]')

        question_image_name = save_uploaded_file(question_image)

        if not question and not question_image_name:
            return render_template(HtmlPageName.crete, item=None, list_id=list_id,
                                   error="Введите вопрос или прикрепите картинку")

        answer_objects = []
        for i, answer_text in enumerate(answers):
            text = answer_text.strip()
            img_name = save_uploaded_file(answer_images[i]) if i < len(answer_images) else None
            if not text and not img_name:
                continue
            answer_objects.append({"text": text, "image": img_name})

        if not answer_objects:
            return render_template(HtmlPageName.crete, item=None, list_id=list_id,
                                   error="Добавьте хотя бы один ответ — текст или картинку")

        right_objects = []
        for i, right_text in enumerate(answers_true):
            text = right_text.strip()
            img_name = save_uploaded_file(answer_true_images[i]) if i < len(answer_true_images) else None
            if not text and not img_name:
                continue
            right_objects.append({"text": text, "image": img_name})

        if not right_objects:
            return render_template(HtmlPageName.crete, item=None, list_id=list_id,
                                   error="Добавьте хотя бы один правильный ответ — текст или картинку")

        Question().save_question(question, answer_objects, right_objects, question_image_name)

        if list_id is not None:
            items = items_load()
            list_file = f'{FileNameAdmin.filename_list_question_file}{list_id}.json'
            update_question_list(list_file, items)
            return redirect(url_for(RedirectHtmlPage.change_blanc_question, list_id=list_id))

        return redirect(url_for(HtmlPageName.index_url))

    return render_template(HtmlPageName.crete, item=None, list_id=list_id, style=get_style, current_topic=get_style)


@app.route('/del_qst/<int:qst_id>')
def del_qs(qst_id):
    get_style = GetTopic(1).get_topic()
    
    Question().delete_qst(qst_id)
    itemss = items_load()
    return render_template(HtmlPageName.index, items=itemss, update=None, style=get_style, current_topic=get_style)


@app.route('/del_qst_list/<int:qst_id>')
def del_qst_list(qst_id):
    get_style = GetTopic(1).get_topic()
    
    Question().delete_qst(qst_id)
    QuestionList().delete_qst(qst_id)

    itemss = items_load(FileNameAdmin.filename_list)
    return render_template(HtmlPageName.question_list, items=itemss, style=get_style, current_topic=get_style)


@app.route('/OpenBlancQuestion')
def all_blanc():
    get_style = GetTopic(1).get_topic()
    
    items = items_load(FileNameAdmin.filename_list)
    return render_template(HtmlPageName.question_list, items=items, style=get_style, current_topic=get_style)


@app.route('/addListQuestion', methods=['GET', 'POST'])
def question_list():
    get_style = GetTopic(1).get_topic()
    
    items = items_load()
    if request.method == 'POST':
        list_name = request.form.get('add_list_question', '').strip()
        if list_name != '':
            h = [x['Qst']['id'] for x in items]

            QuestionList().save_in_list(list_name, h, items)

            return render_template(HtmlPageName.index)
    return render_template(HtmlPageName.index, items=items, style=get_style, current_topic=get_style)


@app.route('/changeBlancQuestion/<int:list_id>')
def change_blanc_question(list_id):
    get_style = GetTopic(1).get_topic()
    
    data = items_load(FileNameAdmin.filename_list)

    matching_items = next(
        (x for x in data if list_id == x['Qst_list']['list_name']), None
    )
    if not matching_items:
        return "Список не найден", 404

    question_list_names = matching_items["Qst_list"]["show_name"]

    filenames = f'{FileNameAdmin.filename_list_question_file}{list_id}.json'

    try:
        with open(filenames, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        questions_data = []

    ChangeQuestionList().update_question_list(questions_data)
    items = items_load()

    return render_template(
        HtmlPageName.index,
        items=items,
        update_button_check=True,
        list_id=list_id,
        question_list_name=question_list_names,
        style=get_style, current_topic=get_style
    )

@app.route('/update-list-question/<int:list_id>', methods=['POST'])
def update_list_question(list_id):
    items = items_load()

    list_file = f'{FileNameAdmin.filename_list_question_file}{list_id}.json'
    result = update_question_list(list_file, items)
    if isinstance(result, Exception):
        logger.error(f"Не удалось обновить лист {list_id}: {result}")

    return redirect(url_for(RedirectHtmlPage.change_blanc_question, list_id=list_id))

@app.route('/changeQuestionAnswer/<int:question_id>', methods=['GET', 'POST'])
def change_question(question_id):
    get_style = GetTopic(1).get_topic()
    
    all_items = items_load()

    question_item = None
    for it in all_items:
        if it.get("Qst", {}).get("id") == question_id:
            question_item = it
            break

    if request.method == 'POST':
        question_text = request.form.get('question', '').strip()
        answers = request.form.getlist('answers[]')
        answers_true = request.form.getlist('answers_true[]')

        cleaned_answers = [a.strip() for a in answers if a.strip()]
        if question_text and cleaned_answers:
            changer = ChangeQuestion(question_id)

            logger.info(question_text)
            logger.info(answers)
            logger.info(answers_true)

            changer.save_question(question_text, answers, answers_true)
            return redirect(url_for(RedirectHtmlPage.index))
        else:
            return render_template(HtmlPageName.change_question_,
                                   item=question_item,
                                   error="Вопрос и хотя бы один ответ обязательны")

    return render_template(HtmlPageName.change_question_, item=question_item, style=get_style, current_topic=get_style)


@app.route('/api/share/<int:question_id>')
def api_share_question(question_id):
    items = items_load()
    for item in items:
        if item.get('Qst', {}).get('id') == question_id:
            question = item['Qst']['question_name']
            answers = item['Qst']['answer']
            right_answers = item['Qst']['right_answer']
            share_url = Url().create_url(question, answers, right_answers, question_id)
            return jsonify({'url': share_url})
    return jsonify({'error': 'Question not found'}), 404


@app.route('/download_question', methods=['POST'])
def download_question():
    question_data = request.form.get('question_data', '').strip()
    question = get_parameter_sing_question(question_data)
    name = question['question']
    answer = question['answer']
    right_answer = question['right_answer']
    question_id = question['question_id']
    Question(question_id).save_question(name, answer, right_answer)

    return redirect(url_for(RedirectHtmlPage.index))


@app.route('/changeImageResultScreen')
def change_image_result_screen():
    get_style = GetTopic(1).get_topic()
    
    images = items_load(FileNameAdmin.filename_image_settings)
    return render_template(HtmlPageName.changeImageResultScreen_html, images=images, style=get_style, current_topic=get_style)


@app.route('/deleteFinallyImageInSave/<int:image_id>')
def delete_finally_image_in_save(image_id):
    get_style = GetTopic(1).get_topic()
    
    DeleteImage().del_image(image_id)
    images = items_load(FileNameAdmin.filename_image_settings)
    return render_template(HtmlPageName.changeImageResultScreen_html, images=images, style=get_style, current_topic=get_style)


@app.route('/use_image/<int:image_id>')
def use_image(image_id):
    print(image_id)
    LoadImage().load_image(image_id)
    return redirect(url_for(RedirectHtmlPage.index))


@app.route('/UploadImage', methods=['POST'])
def upload_image():
    if 'uploadedFile' not in request.files:
        return 'Файл не найден в запросе', 400

    file = request.files['uploadedFile']
    if file.filename == '':
        return 'Файл не выбран', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)

        upload_folder_client = app.config['UPLOAD_FOLDER_CLIENT']
        os.makedirs(upload_folder_client, exist_ok=True)
        file_path_client = os.path.join(upload_folder_client, filename)

        folder_path = Path(FileNameClient.image_path_CLIENT)
        for old_file in folder_path.iterdir():
            if old_file.is_file():
                old_file.unlink()

        file.save(file_path_client)
        shutil.copy2(file_path_client, file_path)
        SaveImage().save(filename)

        return redirect(url_for(RedirectHtmlPage.index))
    else:
        return 'Недопустимый тип файла. Разрешены: ' + ', '.join(app.config['ALLOWED_EXTENSIONS']), 400


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/pass_cut_off', methods=['GET', 'POST'])
def pass_cut_off():
    get_style = GetTopic(1).get_topic()
    
    images = PassCutOff().__load_image_data__()
    value = PassCutOff().__load_result_screen_dict__()
    print(images, value)
    if request.method == 'POST':
        percent = request.form.get('percent-count')
        file = request.files.get('percent_image')
        print(percent)
        print(file)
    return render_template(HtmlPageName.pass_cut_off_html, images=images, values=value, style=get_style, current_topic=get_style)


@app.route('/delete_pass_cut/<int:percent>/<image_name>')
def del_pas_cut_one(percent, image_name):
    get_style = GetTopic(1).get_topic()
    
    PassCutOff().__delete_one_pass_cut__(percent, image_name)

    images = PassCutOff().__load_image_data__()
    value = PassCutOff().__load_result_screen_dict__()

    return render_template(HtmlPageName.pass_cut_off_html, images=images, values=value, style=get_style, current_topic=get_style)


@app.route('/upload-endpoint', methods=['POST'])
def upload_endpoint():
    file = request.files.get('percent_image')
    if file:
        filename = secure_filename(file.filename)
        percent = int(request.form.get('percent-count'))
        print(filename, percent, type(filename), type(percent), ((0 <= percent) and (percent <= 100)), (0 <= percent),
              (0 <= percent <= 100))
        if 0 <= percent <= 100:
            PassCutOff().__save_pass_cut_off__(percent, filename)
            print(SaveImage().save(filename))

            upload_folder = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)

            upload_folder_client = app.config['UPLOAD_FOLDER_CLIENT']
            os.makedirs(upload_folder_client, exist_ok=True)
            file_path_client = os.path.join(upload_folder_client, filename)

            file.save(file_path_client)
            shutil.copy2(file_path_client, file_path)

            return jsonify({'success': True, 'filename': filename})
        return jsonify({'error': "Проценты не могут быть больше 100"}), 400
    return jsonify({'error': 'No file'}), 400


@app.route('/updateIdQuestion')
def update_question_id():
    get_style = GetTopic(1).get_topic()
    
    ChangeQuestionID().change_id()
    item = items_load()
    return render_template(HtmlPageName.index, items=item, style=get_style, current_topic=get_style)


@app.route('/clear-pass-off-file', methods=['POST'])
def clear_pass_off_file():
    if request.method == 'POST':
        if PassCutOff().__clear_file_pass_cut_off__():
            return jsonify({'success': True})

    return jsonify({'error': 'No file'}), 400


@app.route('/settings')
def settings():
    get_style = GetTopic(1).get_topic()

    setting = SettingsPage().load_settings()
    return render_template(HtmlPageName.settings_html, setting=setting, style=get_style, current_topic=get_style)


@app.route("/updateProgram")
def update_program():
    return redirect(url_for(RedirectHtmlPage.index))


@app.route("/set-password", methods=['GET', 'POST'])
def set_password():
    get_style = GetTopic(1).get_topic()
    
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        logger.info(password)
        ChangePassword().change_password(
            file_path_admin=FileNameAdmin.filename_password,
            file_path_loger=FilePathLogApp.file_path_settings,
            file_path_client=FileNameClient.filename_CLIENT_password,
            file_name_log="SettingsLog.log",
            password=password
        )
    return render_template(HtmlPageName.set_password, style=get_style, current_topic=get_style)


@app.route("/lenta", defaults={'topic': False})
@app.route("/shope/", defaults={'topic': True})
def lenta(topic):
    get_style = GetTopic(1).get_topic()
    
    value_check, update_url = cookie(filename=load_question_list_cookie)
    
    logger.info(value_check)
    logger.info(update_url)
    
    if topic:
        lent = get_all_topics()        
        logger.info(lent)
        return render_template(HtmlPageName.lenta_list_question, lent=lent, download_topic_flag=True, style=get_style, current_topic=get_style)
    
    else:
        get_list_question()
        lent = load_question_list()
        
        logger.info(lent)

        return render_template(HtmlPageName.lenta_list_question, lent=lent, download_topic_flag=False, style=get_style, current_topic=get_style)

@app.route("/shope/lenta/Topic/check_list_preview/<int:list_id>", defaults={'topic': True})
@app.route("/lenta/question_list/check_list_preview/<int:list_id>", defaults={'topic': False})
def lenta_check_list_preview(list_id, topic):
    get_style = GetTopic(1).get_topic()
    
    url_question_list = get_url_question_list(list_id)
    url_topic_list = get_url_question_list(list_id)
    logger.info(f"url_question_list={url_question_list!r}")
    logger.info(f"url_topic_list={url_topic_list!r}")

    logger.info(url_topic_list)
    logger.info(topic)
    if topic:
        item = items_load()
        logger.info(url_topic_list)
        current_topic = get_topic(list_id)
        get_style = {"Topic": {"topic_name": "new_style"}}
        logger.info(current_topic)
        return render_template(HtmlPageName.lenta_check_list_preview, items=item, style=get_style, current_topic=current_topic)
        
    else:
        if not url_question_list:
            logger.error(f"Не удалось получить ссылку для list_id={list_id}")
            return "Не удалось получить ссылку на список вопросов", 502

        item = get_list_question(False, url_question_list)
        if item is None:
            logger.error(f"Не удалось загрузить список вопросов для list_id={list_id}")
            return "Не удалось загрузить список вопросов", 502

        return render_template(HtmlPageName.lenta_check_list_preview, items=item, style=get_style, current_topic=get_style)


@app.route("/lenta/question_list/download/<list_name>/<int:list_id>")
@app.route("/lenta/Topic/download/<topic_name>/<int:topic_id>")
@app.route("/shope/lenta/Topic/download/<topic_name>/<int:topic_id>")
def lenta_question_list_download(list_name=None, list_id=None, topic_name=None, topic_id=None):
    url_question_list = get_url_question_list(list_id)
    
    logger.info(f"url_question_list={url_question_list!r}")
    logger.info(f"list_name= {list_name}")
    logger.info(f"list_id= {list_id}")
    logger.info(f"list_id= {list_id}")
    logger.info(f"topic_name= {topic_name}")
    logger.info(f"topic_id= {topic_id}")
    logger.info(f"list_id != None = {list_id != None}")
    
    if topic_name != None:
        all_topic = get_all_topics()
        d = get_topic(topic_id)
        ff = DownloadTopic().download_topic(topic_id=topic_id, all_topic=all_topic)
        with open(f"{file_path_admin}/static/{topic_name}.css", 'w', encoding='utf-8') as f:
            f.write(d)
    
        item = items_load()
        get_style = GetTopic(ff).get_topic_for_id()
        logger.info(get_style)
        return render_template(HtmlPageName.index, items=item, style=get_style, current_topic=get_style)
    elif list_id != None:
        item = get_list_question(False, url_question_list)
        
        h = [x['Qst']['id'] for x in item]

        QuestionList().save_in_list(list_name, h, item)
        blanc = items_load(FileNameAdmin.filename_list)
        get_style = GetTopic(1).get_topic()
        
        return render_template(HtmlPageName.question_list, items=blanc, style=get_style, current_topic=get_style)

@app.route("/change_topic/<int:topic_id>")
def change_topic(topic_id: int):
    ChangeTopic().change_topic()
    itemss = items_load()
    value_check, update_url = cookie()

    logger.info(itemss)
    get_style = GetTopic(1).get_topic()
    
    logger.info(get_style)
    return redirect(url_for(RedirectHtmlPage.index, items=itemss, update=value_check, update_url=update_url, style=get_style, current_topic=get_style))



@app.route("/exitProgram")
def close_program() -> None:
    return windows.destroy()


if __name__ == "__main__":
    now = datetime.now()
    current_time = str(now.strftime("%H:%M %d.%m.%y"))


    FirstRun().create_json_file()

    windows = webview.create_window('Admin', app, fullscreen=True)
    webview.start()

    host = "127.0.0.1"
    port = 5001

    url = f"http://{host}:{port}"
    #app.run(debug=True)
