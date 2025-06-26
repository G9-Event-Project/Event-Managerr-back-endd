from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Global extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///events.db')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": ["https://your-vercel-frontend.vercel.app"]}})

    # Initialize database
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to Community Event Planner API",
            "endpoints": ["/api/register", "/api/login", "/api/events"]
        }), 200

    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    # Import and register blueprints
    from backend.app.routes.auth import auth_bp
    from backend.app.routes.events import events_bp
    from backend.app.routes.comments import comments_bp
    from backend.app.routes.profile import profile_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(events_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')

    return app
