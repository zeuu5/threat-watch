import datetime


def is_sql_injection(username: str) -> bool:
    return "'" in username or " OR " in username.upper()


def is_xss(comment: str) -> bool:
    return "<script" in comment.lower()


def record_request_time(ip: str, request_times: dict) -> datetime.datetime:
    now = datetime.datetime.now()
    request_times.setdefault(ip, []).append(now)
    request_times[ip] = request_times[ip][-10:]
    return now


def detect_rapid_attack(ip: str, request_times: dict, alerts: list) -> None:
    if len(request_times[ip]) >= 5:
        time_diff = (request_times[ip][-1] - request_times[ip][0]).seconds
        if time_diff < 5:
            alerts.append(f"⚡ Rapid attack detected from {ip}")
