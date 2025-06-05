from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Отложенный импорт здесь, чтобы избежать циклического импорта
    from .models import AdminUser

    with app.app_context():
        try:
            db.create_all()
            print("Database tables created or exist")

            # Создаём тестового админа, если его нет
            if not AdminUser.query.filter_by(username="admin").first():
                admin = AdminUser(
                    username="admin",
                    password_hash=generate_password_hash("admin123")
                )
                db.session.add(admin)
                db.session.commit()
                print("Тестовый админ 'admin' создан с паролем 'admin123'")
            else:
                print("Тестовый админ уже существует")

        except Exception as e:
            print("Error connecting to DB:", e)

    from .views import views_bp
    from .auth import auth_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp)

    print("DATABASE_URL:", os.environ.get("DATABASE_URL"))
    return app
