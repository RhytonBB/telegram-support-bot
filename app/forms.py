from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional

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
