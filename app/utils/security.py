import os

LOG_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "logs", "logs.txt")
)
MODE = "VULNERABLE"

failed_attempts = {}
blocked_ips = set()
locked_users = {}
request_times = {}
alerts = []


def get_log_file_path():
    return LOG_FILE
