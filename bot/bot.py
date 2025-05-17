import logging
import threading
from telegram.ext import ApplicationBuilder, CommandHandler
from flask import Flask, send_from_directory, request, jsonify
import os
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


@app_flask.route('/chat/', defaults={'filename': 'index.html'})
@app_flask.route('/chat/<path:filename>')
def chat_static(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'chat'), filename)


@app_flask.route('/<path:path>')
def static_files(path):
    return send_from_directory(WEB_DIR, path)


@app_flask.route("/api/messages/<int:ticket_id>", methods=["GET"])
@app_flask.route("/api/messages/<int:ticket_id>", methods=["GET"])
def get_messages(ticket_id):
    print("ticket_id:", ticket_id)
    ticket = db.get_ticket_by_id(ticket_id)
    print("ticket:", ticket)
    if not ticket:
        return jsonify({"error": f"Ticket {ticket_id} not found"}), 404

    messages = db.get_messages_by_ticket(ticket_id)
    print("messages:", messages)
    return jsonify(messages or [])



@app_flask.route("/api/messages/<int:ticket_id>", methods=["POST"])
def post_message(ticket_id):
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing or invalid JSON body"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Empty message"}), 400

    tg_id = data.get("tg_id", None)

    db.save_message(ticket_id, tg_id, text)
    return jsonify({"status": "ok"}), 201


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

@app.route("/api/tickets")
def api_get_tickets():
    status = request.args.get("status", "new")
    if status not in {"new", "active", "archived"}:
        return jsonify([])

    rows = db.get_tickets_by_status(status)
    return jsonify(rows)


if __name__ == "__main__":
    main()
