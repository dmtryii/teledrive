
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.services import users_services
from app.controllers.users import bp


@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = users_services.get_all()
    json_users= list(map(lambda x: x.to_dict(), users))
    return jsonify({'users': json_users}), 200


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_services.get_by_id(user_id)
    return jsonify({'user': user.to_dict()}), 200


@bp.route('/change_password', methods=['PATCH'])
def change_password_route():
    data = request.get_json()
    user_id = data.get('user_id')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    access_token = users_services.change_password(user_id, current_password, new_password)
    return jsonify(access_token=access_token), 200
