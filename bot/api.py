import os
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from datetime import datetime
from . import db

app = Flask(__name__)

# Конфигурация загрузки файлов
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/messages/<int:ticket_id>", methods=["GET"])
def get_messages(ticket_id):
    messages = db.get_messages_by_ticket(ticket_id)
    if messages is None:
        abort(404)
    return jsonify(messages)

@app.route("/api/messages/<int:ticket_id>", methods=["POST"])
def post_message(ticket_id):
    # Обработка текстовых сообщений
    if request.json:
        data = request.json
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "Empty message"}), 400
        
        db.save_message(
            ticket_id=ticket_id,
            sender="user",
            content=text,
            content_type="text"
        )
        return jsonify({"status": "ok"}), 201
    
    # Обработка загрузки файлов
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            content_type = file.content_type.split('/')[0]  # 'image' или 'video'
            if content_type not in ['image', 'video']:
                content_type = 'file'
            
            db.save_message(
                ticket_id=ticket_id,
                sender="user",
                content=filename,
                content_type=content_type
            )
            
            return jsonify({
                "status": "ok",
                "filename": filename,
                "content_type": content_type
            }), 201
    
    return jsonify({"error": "Invalid request"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)