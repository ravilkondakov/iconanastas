from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime, Text
from gino import Gino

# Base = declarative_base()

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True, index=True)
    username = db.Column(String(255), unique=True, index=True, nullable=False)
    phone = db.Column(String(255), unique=True, index=True, nullable=False)
    password = db.Column(String(255), nullable=False)
    photographer_profile = relationship('Photographer', back_populates='user')


class Photographer(db.Model):
    __tablename__ = 'photographers'

    id = db.Column(Integer, primary_key=True, index=True)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship('User', back_populates='photographer_profile')
    insta_name = db.Column(String(255), unique=True, index=True, nullable=False)
    title = db.Column(String(255), nullable=False)
    date = db.Column(Date, nullable=False, default=datetime.utcnow)
    photoshoots = relationship('Photoshoot', back_populates='photographer')


class Photoshoot(db.Model):
    __tablename__ = 'photoshoots'

    id = db.Column(Integer, primary_key=True, index=True)
    photographer_id = db.Column(Integer, ForeignKey('photographers.id'), nullable=False)
    title = db.Column(String(255), index=True, nullable=False)
    description = db.Column(Text)
    limit = db.Column(Integer, default=15)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    photographer = relationship('Photographer', back_populates='photoshoots')
    comments = relationship('Comment', back_populates='comments')


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(Integer, primary_key=True, index=True)
    photoshoot_id = db.Column(Integer, ForeignKey('photoshoots.id'), nullable=False)
    url = db.Column(String(255), nullable=False)
    description = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(Integer, primary_key=True, index=True)
    photographer_id = db.Column(Integer, ForeignKey('photographers.id'), nullable=False)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    text = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(Integer, primary_key=True, index=True)
    user_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    photoshoot_id = db.Column(Integer, ForeignKey('photoshoots.id'), nullable=False)
    text = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(Integer, primary_key=True, index=True)
    sender_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    text = db.Column(Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
