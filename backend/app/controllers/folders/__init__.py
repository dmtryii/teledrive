from flask import Blueprint

bp = Blueprint('folders', __name__)

from app.controllers.folders import routes