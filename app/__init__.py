import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter

from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.comments import comments_bp


db = SQLAlchemy()
limiter = Limiter(key_func=lambda: request.remote_addr)


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "users.db"))

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(comments_bp)

    with app.app_context():
        from app.models import ensure_default_admin

        db.create_all()
        ensure_default_admin()

    return app


app = create_app()
