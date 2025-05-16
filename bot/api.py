from flask import Flask, request, jsonify, abort
from . import db, config

app = Flask(__name__)

# Убираем функцию check_access, она больше не нужна

@app.route("/api/messages/<int:ticket_id>", methods=["GET"])
def get_messages(ticket_id):
    # tg_id теперь не проверяется
    messages = db.get_messages_by_ticket(ticket_id)
    if messages is None:
        abort(404)  # если тикет не найден или сообщений нет
    return jsonify(messages)

from flask import request

@app.route("/api/messages/<int:ticket_id>", methods=["POST"])
def post_message(ticket_id):
    if request.content_type.startswith("application/json"):
        data = request.json
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        text = data.get("text", "").strip()
        tg_id = data.get("tg_id", None)

    elif request.content_type.startswith("multipart/form-data"):
        text = request.form.get("text", "").strip()
        tg_id = request.form.get("tg_id", None)
        file = request.files.get("file")

        # Обработай файл (сохрани куда нужно) если нужно,
        # сейчас только игнорируем для примера
    else:
        return jsonify({"error": "Unsupported Content-Type"}), 415

    if not text:
        return jsonify({"error": "Empty message"}), 400

    # Сохраняем сообщение в базу (добавь обработку файла если нужно)
    db.save_message(ticket_id, tg_id, text)
    return jsonify({"status": "ok"}), 201
