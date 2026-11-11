import json
import os
import re

from Question.question import QuestionList
from fileModule import *

ANSWERS_WITH_IMAGE = True


def _strip_tail(s: str) -> str:
    for suffix in ('\\:{', '–{', '-{', '\\:', '{'):
        if s.endswith(suffix):
            return s[:-len(suffix)].strip()
    return s.strip()


def parse_gift_string(text: str) -> list[dict]:
    results: list[dict] = []
    current: dict | None = None
    category: str | None = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('//'):
            continue
        if line.startswith('$CATEGORY:'):
            category = line[len('$CATEGORY:'):].strip()
            continue
        if current is None:
            m = re.match(r'^::(.*?)::(.*)$', line)
            if m:
                current = {
                    'category': category,
                    'name':     _strip_tail(m.group(2)),
                    'question': m.group(1).strip(),
                    'correct':  [],
                    'others':   [],
                }
            continue
        if line == '}':
            results.append(current)
            current = None
            continue
        if line.startswith('='):
            current['correct'].append(re.sub(r'^%\d+%', '', line[1:].strip()).strip())
        elif line.startswith('~'):
            current['others'].append(re.sub(r'^%\d+%', '', line[1:].strip()).strip())

    return results


def parse_gift_file(path: str) -> list[dict]:
    with open(path, 'r', encoding='utf-8') as f:
        return parse_gift_string(f.read())


def _format_answers(items: list[str]) -> list:
    if ANSWERS_WITH_IMAGE:
        return [{"text": t, "image": None} for t in items]
    return list(items)


def build_question_list(parsed: list[dict]) -> list[dict]:
    """Собирает все вопросы в один список формата 1.json (id с 1 по порядку)."""
    questions = []
    for i, q in enumerate(parsed, start=1):
        questions.append({
            "Qst": {
                "question_name": q['name'],
                "answer":        _format_answers(q['others']),
                "right_answer":  _format_answers(q['correct']),
                "image":         None,
                "id":            i,
            }
        })
    return questions


def save_parsed_via_question_list(gift_source, show_name: str | None = None) -> None:
    # Qst_list.json должен существовать — иначе qs_id() упадёт
    if not os.path.exists(FileNameAdmin.fillename_QuestionList):
        with open(FileNameAdmin.fillename_QuestionList, 'w', encoding='utf-8') as f:
            f.write('[]')

    if hasattr(gift_source, 'read'):
        raw = gift_source.read()
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8-sig')
        parsed = parse_gift_string(raw)

        filename = getattr(gift_source, 'filename', None)
        if show_name is None and filename:
            show_name = os.path.splitext(os.path.basename(filename))[0]
    else:
        parsed = parse_gift_file(gift_source)
        if show_name is None:
            show_name = os.path.splitext(os.path.basename(gift_source))[0]

    if not parsed:
        print("В файле не найдено ни одного вопроса")
        return

    questions = build_question_list(parsed)

    ql = QuestionList()
    ql.save_in_list(
        name=show_name,
        question_id=[q["Qst"]["id"] for q in questions],
        question_dict=questions,
    )
    print(f"Сохранено {len(questions)} вопросов в {ql.list_filename}")


if __name__ == "__main__":
    save_parsed_via_question_list(
        r"W:\program\QuestionCreatAndRespons\src\admin\1.txt"
    )
