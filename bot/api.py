from flask import Flask, request, jsonify, abort
from bot import db

app = Flask(__name__)

@app.route("/api/messages/<int:ticket_id>", methods=["GET"])
def get_messages(ticket_id):
    messages = db.get_messages_by_ticket(ticket_id)
    if messages is None:
        abort(404)
    return jsonify(messages)

@app.route("/api/messages/<int:ticket_id>", methods=["POST"])
def post_message(ticket_id):
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Empty message"}), 400

    # tg_id можно не использовать или брать из data для совместимости
    tg_id = data.get("tg_id", None)

    db.save_message(ticket_id, tg_id, text)
    return jsonify({"status": "ok"}), 201
