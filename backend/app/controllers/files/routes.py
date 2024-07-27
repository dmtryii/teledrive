
import requests

from config import Config
from app.models.files import File
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.controllers.files import bp
from app.extensions import db


TELEGRAM_BOT_TOKEN = Config.BOT_TOKEN
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'


@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'files' not in request.files:
        return jsonify({"msg": "No files part"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"msg": "No selected files"}), 400

    user_id = get_jwt_identity()
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue

        filename = file.filename

        url = f"{TELEGRAM_API_URL}/sendDocument"
        telegram_files = {
            'document': (filename, file),
        }
        data = {
            'chat_id': user_id
        }

        response = requests.post(url, files=telegram_files, data=data)

        if response.status_code != 200:
            return jsonify({"msg": f"Telegram API error for file {filename}: {response.text}"}), 500

        telegram_response = response.json()
        telegram_file_id = telegram_response['result']['document']['file_id']

        new_file = File(
            name=filename,
            telegram_file_id=telegram_file_id,
            user_id=user_id
        )
        db.session.add(new_file)
        uploaded_files.append(filename)

    db.session.commit()

    return jsonify({"msg": "Files uploaded successfully", "files": uploaded_files}), 201


@bp.route('/<int:file_id>/download', methods=['GET'])
@jwt_required()
def download_file(file_id):
    file = File.query.get(file_id)
    if not file or file.user_id != get_jwt_identity():
        return jsonify({"msg": "File not found or unauthorized"}), 404
    
    url = f"{TELEGRAM_API_URL}/getFile"
    params = {
        'file_id': file.telegram_file_id
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify({"msg": f"Telegram API error: {response.text}"}), 500
    
    file_path = response.json()['result']['file_path']
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
    
    return jsonify({"file_url": file_url})


@bp.route('/', methods=['GET'])
@jwt_required()
def list_files():
    user_id = get_jwt_identity()
    files = File.query.filter_by(user_id=user_id).all()
    return jsonify([file.to_dict() for file in files])


@bp.route('/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    file = File.query.get(file_id)
    if not file or file.user_id != get_jwt_identity():
        return jsonify({"msg": "File not found or unauthorized"}), 404
    
    db.session.delete(file)
    db.session.commit()
    
    return jsonify({"msg": "File deleted successfully"}), 200
