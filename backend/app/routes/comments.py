from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db, limiter
from backend.app.models import Event, Comment

comments_bp = Blueprint('comments', __name__)

# Get comments for a specific event
@comments_bp.route('/comments/event/<int:event_id>', methods=['GET'])
@jwt_required()
def get_comments(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    comments = Comment.query.filter_by(event_id=event_id).all()
    return jsonify([comment.to_dict() for comment in comments]), 200

# Add a comment to an event
@comments_bp.route('/comments/event/<int:event_id>', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def add_comment(event_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'content' not in data or not data['content'].strip():
        return jsonify({"error": "Content is required"}), 400

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    comment = Comment(
        content=data['content'],
        event_id=event_id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201
