from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db, bcrypt, limiter
from app.models import User

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# View own profile
@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    user = User.query.get_or_404(get_jwt_identity())
    return jsonify(user.to_dict()), 200

# Update profile
@profile_bp.route('/', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per minute")
def update_profile():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_username = data.get('username', user.username)
    new_email = data.get('email', user.email)
    
    if new_username != user.username and User.query.filter_by(username=new_username).first():
        return jsonify({"error": "Username already exists"}), 400
    if new_email != user.email and User.query.filter_by(email=new_email).first():
        return jsonify({"error": "Email already exists"}), 400

    user.username = new_username
    user.email = new_email

    if 'password' in data and data['password'].strip():
        if len(data['password']) < 6:
            return jsonify({"error": "Password too short"}), 400
        user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    db.session.commit()
    return jsonify(user.to_dict()), 200
