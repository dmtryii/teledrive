
from flask import jsonify
from app.controllers.users import bp
from app.exceptions.custom_exception import CustomException


@bp.errorhandler(CustomException)
def handle_custom_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
