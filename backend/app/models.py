from backend.app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    events = relationship('Event', backref='creator', lazy=True)
    comments = relationship('Comment', backref='author', lazy=True)
    participations = relationship('Participant', backref='user', lazy=True)

    def set_password(self, password):
        from app import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def check_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password.encode('utf-8'))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Event(db.Model):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    location = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = relationship('Comment', backref='event', lazy=True)
    participants = relationship('Participant', backref='event', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class Participant(db.Model):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    rsvp_status = Column(String(20), nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)