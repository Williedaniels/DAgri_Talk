from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy.exc import IntegrityError
from app.models.knowledge import KnowledgeEntry

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('/', methods=['POST'])
@jwt_required()
def create_knowledge_entry():
    data = request.get_json()
    author_id = get_jwt_identity()

    required_fields = ['title', 'content']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'message': 'Missing required fields: title and content'}), 400

    try:
        entry = KnowledgeEntry(
            title=data['title'],
            content=data['content'],
            language=data.get('language', 'English'),
            crop_type=data.get('crop_type'),
            season=data.get('season'),
            region=data.get('region'),
            author_id=author_id
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify(entry.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Database error, possibly invalid author.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create knowledge entry', 'error': str(e)}), 500

@knowledge_bp.route('/', methods=['GET'])
def get_knowledge_entries():
    try:
        entries = KnowledgeEntry.query.order_by(KnowledgeEntry.created_at.desc()).all()
        return jsonify([entry.to_dict() for entry in entries]), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve knowledge entries', 'error': str(e)}), 500