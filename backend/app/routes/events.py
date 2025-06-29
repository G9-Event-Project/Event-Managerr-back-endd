from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import Event
from backend.app import db, limiter
from datetime import datetime

events_bp = Blueprint('events', __name__)

# GET all events
@events_bp.route('/', methods=['GET'])
@jwt_required()
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200

# GET one event
@events_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify(event.to_dict()), 200

# POST create event
@events_bp.route('/', methods=['POST'])
@jwt_required()
@limiter.limit("5 per minute", key_func=get_jwt_identity)
def create_event():
    data = request.get_json()
    current_user = get_jwt_identity()

    if not data or not all(k in data for k in ['title', 'date']):
        return jsonify({"error": "Missing title or date"}), 400

    try:
        event = Event(
            title=data['title'],
            description=data.get('description', ''),
            location=data.get('location', ''),
            date=datetime.strptime(data['date'], "%Y-%m-%d"),
            user_id=current_user
        )
        db.session.add(event)
        db.session.commit()
        return jsonify(event.to_dict()), 201
    except ValueError:
        return jsonify({"error": "Invalid date format (use YYYY-MM-DD)"}), 400

# PUT update event
@events_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_event(id):
    event = Event.query.get_or_404(id)
    current_user = get_jwt_identity()

    if event.user_id != current_user:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.location = data.get("location", event.location)

    if 'date' in data:
        try:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format (use YYYY-MM-DD)"}), 400

    event.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(event.to_dict()), 200

# DELETE event
@events_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    event = Event.query.get_or_404(id)
    current_user = get_jwt_identity()

    if event.user_id != current_user:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200

# SEARCH
@events_bp.route('/search', methods=['GET'])
@limiter.limit("10 per minute")
def search():
    keyword = request.args.get('q', '')
    events = Event.query.filter(
        Event.title.ilike(f'%{keyword}%') |
        Event.description.ilike(f'%{keyword}%') |
        Event.location.ilike(f'%{keyword}%')
    ).all()
    return jsonify([event.to_dict() for event in events]), 200
