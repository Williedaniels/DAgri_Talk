from app import db
from datetime import datetime

class KnowledgeEntry(db.Model):
    __tablename__ = 'knowledge_entry'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), default='English')
    crop_type = db.Column(db.String(100))
    season = db.Column(db.String(50))
    region = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship('User', backref=db.backref('knowledge_entries', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'language': self.language,
            'crop_type': self.crop_type,
            'season': self.season,
            'region': self.region,
            'author_id': self.author_id,
            'author_username': self.author.username if self.author else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }