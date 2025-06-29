from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///events.db')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from backend.app.models import User, Event, Comment, Participant

    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to Community Event Planner API",
            "endpoints": ["/api/register", "/api/login", "/api/events"]
        }), 200

    @app.route('/favicon.ico')
    def favicon():
        return '', 204
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response



    from backend.app.routes.auth import auth_bp
    from backend.app.routes.events import events_bp
    from backend.app.routes.comments import comments_bp
    from backend.app.routes.profile import profile_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(events_bp, url_prefix='/api/events')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')

    return app
