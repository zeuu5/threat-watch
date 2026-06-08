from werkzeug.security import generate_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


def ensure_default_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        default_password = generate_password_hash("password123")
        admin = User(username="admin", password=default_password)
        db.session.add(admin)
        db.session.commit()
