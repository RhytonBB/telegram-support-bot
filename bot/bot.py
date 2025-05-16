import logging
import threading
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask, send_from_directory
import os
from flask import request
from . import config, db, handlers

# === Flask-сервер для отдачи веб-интерфейса ===

app_flask = Flask(__name__)
WEB_DIR = os.path.join(os.path.dirname(__file__), '..', 'web')

@app_flask.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')

@app_flask.route('/operators.html')
def operators():
    return send_from_directory(WEB_DIR, 'operators.html')

@app_flask.route('/chat')
def chat():
    return send_from_directory(os.path.join(WEB_DIR, 'chat'), 'index.html')

@app_flask.route('/<path:path>')
def static_files(path):
    return send_from_directory(WEB_DIR, path)

@app_flask.route('/chat/<path:filename>')
def chat_static(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'chat'), filename)

@app_flask.route("/api/messages/<int:ticket_id>")
def get_messages(ticket_id):
    tg_id = request.args.get("tg_id")
    ticket = db.get_ticket(ticket_id)
    if not ticket or ticket["user_tg_id"] != tg_id:
        return jsonify({"error": "Unauthorized"}), 403



def run_flask():
    app_flask.run(host='0.0.0.0', port=8080)


# === Telegram-бот ===

def main():
    # Инициализация базы данных
    db.init_db()

    # Логирование
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Запуск Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()

    # Создание приложения Telegram
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Регистрация хендлеров
    handlers.register_handlers(app)

    # Обработка команды /start (приветствие + кнопка)
    async def start(update, context):
        await update.message.reply_text(
            "Привет! Нажмите /support для обращения в техподдержку."
        )

    app.add_handler(CommandHandler("start", start))

    # Запуск бота
    logging.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
