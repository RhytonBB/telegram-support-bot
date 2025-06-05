from . import db
from flask_login import UserMixin

class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Executor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64), nullable=True)
    passport = db.Column(db.String(64))
    inn = db.Column(db.String(64))
    company = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    telegram_nick = db.Column(db.String(64), unique=True)
    access_key = db.Column(db.String(64), unique=True)
    is_verified = db.Column(db.Boolean, default=False)
    fail_attempts = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Boolean, default=False)
