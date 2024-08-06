
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.controllers.files import bp
from app.exceptions.file_exception import FileUploadError
from app.services import file_service


@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_files():
    if 'files' not in request.files:
        raise FileUploadError(message='No files part')

    files = request.files.getlist('files')
    if not files:
        raise FileUploadError(message='No selected file')

    user_id = get_jwt_identity()
    try:
        uploaded_files = file_service.upload_files(files, user_id)
        return jsonify({"msg": "Files uploaded successfully", "files": uploaded_files}), 201
    except Exception as e:
        return jsonify({"msg": f"Unexpected error: {str(e)}"}), 500


@bp.route('/<int:file_id>/download', methods=['GET'])
@jwt_required()
def download_file(file_id):
    user_id = get_jwt_identity()
    try:
        file_url = file_service.download_file(file_id, user_id)
        return jsonify({"file_url": file_url}), 200
    except Exception as e:
        return jsonify({"msg": f"Unexpected error: {str(e)}"}), 500


@bp.route('/', methods=['GET'])
@jwt_required()
def get_files():
    user_id = get_jwt_identity()
    files = file_service.get_files(user_id)
    return jsonify([file.to_dict() for file in files]), 200


@bp.route('<int:file_id>/move', methods=['POST'])
@jwt_required()
def move_file(file_id):
    user_id = get_jwt_identity()
    folder_id = request.json.get('folder_id')

    try:
        file = file_service.set_file_folder(user_id, file_id, folder_id)
        return jsonify(file.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": f"Unexpected error: {str(e)}"}), 500


@bp.route('/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    user_id = get_jwt_identity()
    try:
        file_service.delete_file(file_id, user_id)
        return jsonify({"msg": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": f"Unexpected error: {str(e)}"}), 500
