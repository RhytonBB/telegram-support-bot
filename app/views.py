from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required
from .forms import ExecutorForm, OrderForm
from .models import Executor, Order
from . import db
import secrets

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
@login_required
def index():
    return redirect(url_for("views.register_executor"))

@views_bp.route("/register", methods=["GET", "POST"])
@login_required
def register_executor():
    form = ExecutorForm()
    if form.validate_on_submit():
        access_key = secrets.token_hex(4).upper()
        executor = Executor(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            passport=form.passport.data,
            inn=form.inn.data,
            company=form.company.data,
            phone=form.phone.data,
            telegram_nick=form.telegram_nick.data,
            access_key=access_key
        )
        db.session.add(executor)
        db.session.commit()
        flash(f"Исполнитель зарегистрирован. Ключ доступа: {access_key}", "success")
        return redirect(url_for("views.register_executor"))
    return render_template("register.html", form=form)

@views_bp.route("/create-order", methods=["GET", "POST"])
@login_required
def create_order():
    # Проверяем наличие исполнителей в базе
    executors = Executor.query.all()
    current_app.logger.info(f"Total executors in database: {len(executors)}")
    for executor in executors:
        current_app.logger.info(f"Executor: {executor.last_name} {executor.first_name} ({executor.telegram_nick})")

    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            telegram_nick=form.executor.data,
            title=form.title.data,
            description=form.description.data,
            photo_file_id=None,
            status='active'
        )
        db.session.add(order)
        db.session.commit()
        flash("Заказ успешно создан", "success")
        return redirect(url_for("views.create_order"))
    return render_template("create_order.html", form=form)
