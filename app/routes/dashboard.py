from flask import Blueprint, render_template
from app.utils.logger import read_logs
from app.utils.security import alerts

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/logs")
def view_logs():
    logs = read_logs()
    total = len(logs)
    fails = sum("FAIL" in log for log in logs)
    sqli = sum("SQL_INJECTION" in log for log in logs)
    xss = sum("XSS_ATTACK" in log for log in logs)

    return render_template(
        "dashboard.html",
        logs=logs,
        total=total,
        fails=fails,
        sqli=sqli,
        xss=xss,
        attack_counts=[fails, sqli, xss],
        alerts=alerts[-5:],
    )
