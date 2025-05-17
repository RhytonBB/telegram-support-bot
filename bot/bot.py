import logging
import threading
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask, send_from_directory
import os
from . import config, db, handlers

# Flask приложение для веб-интерфейса
app_flask = Flask(__name__)
WEB_DIR = os.path.join(os.path.dirname(__file__), '..', 'web')

# Маршруты для статических файлов
@app_flask.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')

@app_flask.route('/operators.html')
def operators():
    return send_from_directory(WEB_DIR, 'operators.html')

@app_flask.route('/chat/<path:filename>')
def chat_files(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'chat'), filename)

@app_flask.route('/<path:path>')
def static_files(path):
    return send_from_directory(WEB_DIR, path)

def run_flask():
    app_flask.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )

def main():
    # Инициализация
    db.init_db()
    
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Запуск Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Telegram бот
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    handlers.register_handlers(application)
    
    logging.info("Сервис запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()