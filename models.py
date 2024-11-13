from datetime import datetime
from app import db

class Context(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    specifications = db.Column(db.Text)
    generated_code = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    error_message = db.Column(db.Text)

class GeneratedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    context_id = db.Column(db.Integer, db.ForeignKey('context.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
