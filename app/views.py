from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from .forms import ExecutorForm
from .models import Executor
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
