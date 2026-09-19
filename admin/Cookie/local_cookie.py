# -*- coding: utf-8 -*-
import json
from datetime import datetime
from loguru import logger
from Cookie.SessionKey import time_check_update, Value_Check
from fileModule import filename_cookie
from Settings.UpdateProgram.update import Update


def set_session(time_check_updates, value_Check):

    data = {
        time_check_update: time_check_updates.strftime("%H:%M %d.%m.%y"),
        Value_Check: bool(value_Check)
    }
    try:
        with open(filename_cookie, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Session saved: {data}")
    except Exception as e:
        logger.error(f"Failed to save session: {e}")


def get_session():
    try:
        with open(filename_cookie, 'r', encoding='utf-8') as f:
            data = json.load(f)
        time_str = data.get(time_check_update)
        value = data.get(Value_Check)
        if value is not None:
            value = bool(value)
        else:
            value = False
        return time_str, value
    except FileNotFoundError:
        default_time = datetime.now().strftime("%H:%M %d.%m.%y")
        default_value = False
        set_session(datetime.now(), default_value)
        return default_time, default_value
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error reading session: {e}")
        return None, None


def update_session():
    now = datetime.now()
    time_str, current_value = get_session()

    if time_str is None:
        logger.warning("Session time is invalid, forcing check.")
        value_check = Update().all_check()
        set_session(now, value_check)
        return value_check

    try:
        last_time = datetime.strptime(time_str, "%H:%M %d.%m.%y")
    except ValueError:
        logger.warning("Session time format invalid, forcing check.")
        value_check = Update().all_check()
        set_session(now, value_check)
        return value_check

    if (now - last_time).total_seconds() >= 25 * 60:
        logger.info("Time to re-check for updates.")
        value_check = Update().all_check()
        set_session(now, value_check)
        return value_check
    else:
        return current_value
