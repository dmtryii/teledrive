from flask import Flask, jsonify
from flask_cors import CORS

from app.exceptions.custom_exception import CustomException
from config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # JWT    
    jwt.init_app(app)
    
    # Register blueprints
    from app.controllers.users import bp as users_bp
    from app.controllers.auth import bp as auth_bp
    from app.controllers.files import bp as files_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(files_bp, url_prefix='/api/files')
        
    # Register error handlers
    app.register_error_handler(CustomException, handle_custom_exception)
        
    return app


def handle_custom_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
