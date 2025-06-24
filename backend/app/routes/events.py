from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Event
from datetime import datetime

events_bp = Blueprint('events', __name__, url_prefix='/events')

# GET all events (with optional search query)
@events_bp.route('/', methods=['GET'])
def get_events():
    search = request.args.get('search', '')
    events = Event.query.filter(Event.title.ilike(f"%{search}%")).all()
    return jsonify([event.to_dict() for event in events]), 200

# GET one event
@events_bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify(event.to_dict()), 200

# POST create event
@events_bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    current_user = get_jwt_identity()

    try:
        event = Event(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            date=datetime.strptime(data['date'], "%Y-%m-%d"),
            user_id=current_user
        )
        db.session.add(event)
        db.session.commit()
        return jsonify(event.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
        event.date = datetime.strptime(data['date'], "%Y-%m-%d")

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
