from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Comment, Event

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

# Get comments for a specific event
@comments_bp.route('/event/<int:event_id>', methods=['GET'])
def get_comments(event_id):
    comments = Comment.query.filter_by(event_id=event_id).all()
    return jsonify([c.to_dict() for c in comments]), 200

# Add a comment to an event
@comments_bp.route('/event/<int:event_id>', methods=['POST'])
@jwt_required()
def add_comment(event_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    comment = Comment(
        content=data['content'],
        event_id=event_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201
