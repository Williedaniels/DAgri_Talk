from datetime import datetime
from bson.objectid import ObjectId

"""
Knowledge Entry document structure:
{
    _id: ObjectId,
    title: String,
    content: String,
    language: String,
    crop_type: String,
    season: String,
    region: String,
    author_id: ObjectId,
    created_at: DateTime,
    updated_at: DateTime
}
"""

def create_knowledge_entry(mongo, title, content, author_id, language=None, 
                         crop_type=None, season=None, region=None):
    """Create a new knowledge entry document"""
    now = datetime.utcnow()
    entry = {
        'title': title,
        'content': content,
        'language': language,
        'crop_type': crop_type,
        'season': season,
        'region': region,
        'author_id': ObjectId(author_id),
        'created_at': now,
        'updated_at': now
    }
    return mongo.db.knowledge_entries.insert_one(entry)

def get_knowledge_entry(mongo, entry_id):
    """Get knowledge entry by ID"""
    if isinstance(entry_id, str):
        entry_id = ObjectId(entry_id)
    return mongo.db.knowledge_entries.find_one({'_id': entry_id})

def get_all_knowledge_entries(mongo):
    """Get all knowledge entries"""
    return list(mongo.db.knowledge_entries.find())

def knowledge_entry_to_dict(mongo, entry):
    """Convert knowledge entry to dictionary for API responses"""
    author = mongo.db.users.find_one({'_id': entry['author_id']})
    author_username = author['username'] if author else None
    
    return {
        'id': str(entry['_id']),
        'title': entry['title'],
        'content': entry['content'],
        'language': entry.get('language'),
        'crop_type': entry.get('crop_type'),
        'season': entry.get('season'),
        'region': entry.get('region'),
        'author_id': str(entry['author_id']),
        'author_username': author_username,
        'created_at': entry['created_at'].isoformat(),
        'updated_at': entry['updated_at'].isoformat()
    }