from flask import jsonify, request

from app.controllers.auth import bp
from app.services import auth_service


@bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()    
    access_token = auth_service.signin(
        user_id=int(data.get('user_id')),
        password=data.get('password')
    )
    return jsonify(access_token=access_token), 200


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    access_token = auth_service.signup(
        user_id=int(data.get('user_id')),
        username=data.get('username'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    return jsonify(access_token=access_token), 201
