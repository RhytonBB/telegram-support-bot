from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from .models import AdminUser
from .forms import LoginForm
from . import login_manager, db

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("views.register_executor"))
        flash("Неверный логин или пароль", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
