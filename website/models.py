from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    log_status = db.Column(db.Integer, default=0)
    notes = db.relationship('Note', backref='user', lazy=True)
    settings = db.relationship('Settings', backref='user', uselist=False, lazy=True)
    access_logs = db.relationship('AccessLog', backref='user', lazy=True)

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    backups = db.relationship('Backup', backref='note', lazy=True)

class AccessLog(db.Model):
    __tablename__ = 'access_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    theme = db.Column(db.String(20), default='light')
    font_size = db.Column(db.String(10), default='medium')
    notes_per_page = db.Column(db.Integer, default=10)
    email_notifications = db.Column(db.Boolean, default=False)

class Backup(db.Model):
    __tablename__ = 'backup'
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
