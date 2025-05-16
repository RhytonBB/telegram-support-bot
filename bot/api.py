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

@app.route("/api/messages/<int:ticket_id>", methods=["POST"])
def post_message(ticket_id):
    # tg_id не проверяем
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Empty message"}), 400

    # Сохраняем сообщение
    # Для совместимости, если нужно tg_id, можно брать из data или None
    tg_id = data.get("tg_id", None)

    db.save_message(ticket_id, tg_id, text)
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(port=config.API_PORT)
