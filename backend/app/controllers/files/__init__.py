from flask import Blueprint

bp = Blueprint('files', __name__)

from app.controllers.files import routes