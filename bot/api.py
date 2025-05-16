from flask import Flask, request, jsonify, abort
from . import db, config

app = Flask(__name__)

def chat():
    return send_from_directory(os.path.join(WEB_DIR, 'chat'), 'index.html')
    
# Проверка Telegram ID и обращения
def check_access(tg_id: str, ticket_id: int) -> bool:
    # Здесь проверяем, что обращение принадлежит пользователю с tg_id
    ticket = db.get_ticket_by_id(ticket_id)
    return ticket and str(ticket['tg_id']) == tg_id

@app.route("/api/messages/<int:ticket_id>", methods=["GET"])
def get_messages(ticket_id):
    tg_id = request.args.get("tg_id")
    if not tg_id or not check_access(tg_id, ticket_id):
        abort(403)
    messages = db.get_messages_by_ticket(ticket_id)
    return jsonify(messages)

@app.route("/api/messages/<int:ticket_id>", methods=["POST"])
def post_message(ticket_id):
    tg_id = request.args.get("tg_id")
    if not tg_id or not check_access(tg_id, ticket_id):
        abort(403)
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Empty message"}), 400
    # Сохраняем сообщение
    db.save_message(ticket_id, tg_id, text)
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(port=config.API_PORT)
