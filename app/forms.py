from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional
from .models import Executor, Worker
from flask import current_app

class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

class ExecutorForm(FlaskForm):
    last_name = StringField("Фамилия", validators=[DataRequired()])
    first_name = StringField("Имя", validators=[DataRequired()])
    middle_name = StringField("Отчество", validators=[Optional()])
    passport = StringField("Паспортные данные", validators=[DataRequired()])
    inn = StringField("ИНН", validators=[DataRequired()])
    company = StringField("Компания", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired()])
    telegram_nick = StringField("Telegram ник", validators=[DataRequired()])
    submit = SubmitField("Зарегистрировать исполнителя")

class OrderForm(FlaskForm):
    executor = SelectField("Работник", coerce=str, validators=[DataRequired()])
    title = StringField("Название заказа", validators=[DataRequired()])
    description = TextAreaField("Описание заказа", validators=[DataRequired()])
    submit = SubmitField("Создать заказ")

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        try:
            # Получаем всех работников
            workers = Worker.query.all()
            if workers:
                self.executor.choices = [(w.telegram_nick, f"{w.full_name} ({w.telegram_nick})") for w in workers]
                current_app.logger.info(f"Found {len(workers)} workers")
            else:
                self.executor.choices = [("", "Нет доступных работников")]
                current_app.logger.warning("No workers found in database")
        except Exception as e:
            current_app.logger.error(f"Error loading workers: {str(e)}")
            self.executor.choices = [("", "Ошибка загрузки списка работников")]
