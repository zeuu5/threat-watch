from flask import Blueprint, request, render_template
from werkzeug.security import check_password_hash

from app import limiter
from app.models import User
from app.utils.detector import detect_rapid_attack, is_sql_injection, record_request_time
from app.utils.logger import log_attempt
from app.utils.security import (
    MODE,
    blocked_ips,
    failed_attempts,
    locked_users,
    request_times,
    alerts,
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    message = None

    if request.method == "POST":
        ip = request.remote_addr
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if MODE == "SECURE" and ip in blocked_ips:
            message = "🚫 Access blocked (IP flagged)"
            return render_template("login.html", message=message)

        failed_attempts.setdefault(username, 0)
        record_request_time(ip, request_times)
        detect_rapid_attack(ip, request_times, alerts)

        if is_sql_injection(username):
            log_attempt(ip, username, password, "SQL_INJECTION")
            alerts.append(f"💉 SQL Injection attempt from {ip}")
            message = "Login successful"
            return render_template("login.html", message=message)

        if username in locked_users:
            message = "🔒 Account locked due to suspicious activity"
            return render_template("login.html", message=message)

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            log_attempt(ip, username, password, "SUCCESS")
            failed_attempts[username] = 0
            message = "Login successful"
            return render_template("login.html", message=message)

        failed_attempts[username] += 1
        log_attempt(ip, username, password, "FAIL")

        if failed_attempts[username] >= 5:
            alerts.append(f"🚨 Brute force on {username} from {ip}")
            locked_users[username] = True
            blocked_ips.add(ip)

        message = "Login failed"

    return render_template("login.html", message=message)
