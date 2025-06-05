from . import db
from flask_login import UserMixin
from datetime import datetime

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
    telegram_nick = db.Column(db.String(64), unique=True, nullable=False)  # Ключ связи
    access_key = db.Column(db.String(64), unique=True)
    is_verified = db.Column(db.Boolean, default=False)
    fail_attempts = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Boolean, default=False)

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_nick = db.Column(db.String(64), db.ForeignKey('executor.telegram_nick'), nullable=False)
    executor = db.relationship('Executor', backref=db.backref('workers', lazy=True),
                               primaryjoin="Worker.telegram_nick == Executor.telegram_nick")

    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    full_name = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    is_blocked = db.Column(db.Boolean, default=False)
    fail_attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_nick = db.Column(db.String(64), db.ForeignKey('executor.telegram_nick'), nullable=False)
    executor = db.relationship('Executor', backref=db.backref('orders', lazy=True),
                               primaryjoin="Order.telegram_nick == Executor.telegram_nick")

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    photo_file_id = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(16), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.CheckConstraint("status IN ('active', 'completed')", name='valid_status'),
    )
