import os
from datetime import datetime
from app.utils.security import get_log_file_path


def log_attempt(ip, username, password, result):
    log_file = get_log_file_path()
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {ip} | {username} | {password} | {result}\n")


def read_logs():
    log_file = get_log_file_path()
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    return [line.strip() for line in lines[::-1]]
