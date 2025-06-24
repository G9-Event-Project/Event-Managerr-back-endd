from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# View own profile
@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    user = User.query.get(get_jwt_identity())
    return jsonify(user.to_dict()), 200

# Update profile
@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    user = User.query.get(get_jwt_identity())
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    db.session.commit()
    return jsonify(user.to_dict()), 200
