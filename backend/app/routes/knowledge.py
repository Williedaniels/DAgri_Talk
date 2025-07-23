from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('/', methods=['GET'])
def get_knowledge():
    try:
        db = get_db()
        entries = list(db.knowledge_entries.find())
        
        # Convert ObjectId to string for JSON serialization
        for entry in entries:
            entry['_id'] = str(entry['_id'])
            if 'author_id' in entry and entry['author_id']:
                entry['author_id'] = str(entry['author_id'])
            
            # Format dates for JSON serialization
            if 'created_at' in entry:
                entry['created_at'] = entry['created_at'].isoformat()
            if 'updated_at' in entry:
                entry['updated_at'] = entry['updated_at'].isoformat()
                
            # Add author username if possible
            if 'author_id' in entry and entry['author_id']:
                author = db.users.find_one({'_id': ObjectId(entry['author_id'])})
                entry['author_username'] = author['username'] if author else 'Unknown'
        
        return jsonify(entries), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching knowledge entries: {str(e)}")
        return jsonify({'message': 'Error fetching knowledge entries', 'error': str(e)}), 500

@knowledge_bp.route('/', methods=['POST'])
@jwt_required()
def create_knowledge():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        now = datetime.utcnow()
        new_entry = {
            'title': data['title'],
            'content': data['content'],
            'author_id': ObjectId(user_id) if user_id else None,
            'language': data.get('language'),
            'crop_type': data.get('crop_type'),
            'season': data.get('season'),
            'region': data.get('region'),
            'created_at': now,
            'updated_at': now
        }
        
        db = get_db()
        result = db.knowledge_entries.insert_one(new_entry)
        
        # Get the newly created entry
        entry = db.knowledge_entries.find_one({'_id': result.inserted_id})
        
        # Prepare response
        entry['_id'] = str(entry['_id'])
        if 'author_id' in entry and entry['author_id']:
            entry['author_id'] = str(entry['author_id'])
        if 'created_at' in entry:
            entry['created_at'] = entry['created_at'].isoformat()
        if 'updated_at' in entry:
            entry['updated_at'] = entry['updated_at'].isoformat()
        
        # Add author username
        author = db.users.find_one({'_id': ObjectId(user_id)}) if user_id else None
        entry['author_username'] = author['username'] if author else 'Unknown'
        
        return jsonify(entry), 201
    except Exception as e:
        current_app.logger.error(f"Error creating knowledge entry: {str(e)}")
        return jsonify({'message': 'Failed to create knowledge entry', 'error': str(e)}), 500