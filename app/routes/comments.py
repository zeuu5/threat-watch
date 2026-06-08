from flask import Blueprint, request, render_template

from app.utils.logger import log_attempt
from app.utils.detector import is_xss

comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        user_comment = request.form.get("comment", "")
        ip = request.remote_addr

        if is_xss(user_comment):
            log_attempt(ip, "XSS_USER", user_comment, "XSS_ATTACK")
            return render_template("comment.html", message="💬 XSS attempt detected and logged.")

        return render_template("comment.html", message=f"Comment received: {user_comment}")

    return render_template("comment.html")
