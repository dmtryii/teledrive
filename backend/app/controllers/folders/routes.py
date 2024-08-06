
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.controllers.folders import bp
from app.services import folder_services


@bp.route('/', methods=['GET'])
@jwt_required()
def get_root_folder():
    user_id = get_jwt_identity()
    root_folder = folder_services.get_root_folder(user_id)
    return jsonify(root_folder.to_dict()), 200


@bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_folders():
    user_id = get_jwt_identity()
    folders = folder_services.get_all_folders(user_id)
    return jsonify([folder.to_dict() for folder in folders]), 200


@bp.route('/<int:folder_id>', methods=['GET'])
@jwt_required()
def get_folder(folder_id):
    user_id = get_jwt_identity()
    folder = folder_services.get_folder(user_id, folder_id)
    return jsonify(folder.to_dict()), 200


@bp.route('/', methods=['POST'])
@jwt_required()
def create_folder():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_folder = folder_services.create_folder(
        name=data.get('name'),
        user_id=user_id,
        parent_id=int(data.get('parent_id')) if data.get('parent_id') else None
    )
    return jsonify(new_folder=new_folder.to_dict()), 201


@bp.route('/<int:folder_id>', methods=['DELETE'])
@jwt_required()
def delete_folder(folder_id):
    user_id = get_jwt_identity()
    folder_services.delete_folder(user_id, folder_id)
    return jsonify({'message': 'Folder deleted successfully'}), 200


@bp.route('/move', methods=['POST'])
@jwt_required()
def move_folder():
    user_id = get_jwt_identity()
    data = request.get_json()
    folder = folder_services.move_folder(
        user_id=user_id,
        folder_id=data.get('folder_id'),
        destination_folder_id=data.get('destination_folder_id')
    )
    return jsonify(folder.to_dict()), 200


@bp.route('/<int:folder_id>/available_to_move', methods=['GET'])
@jwt_required()
def available_to_move(folder_id):
    user_id = get_jwt_identity()
    folders = folder_services.get_all_available_to_move(
        user_id=user_id,
        folder_id=folder_id,
    )
    return jsonify([folder.to_dict() for folder in folders]), 200
