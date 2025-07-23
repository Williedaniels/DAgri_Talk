from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime

"""
User document structure:
{
    _id: ObjectId,
    username: String,
    email: String,
    password_hash: String,
    user_type: String,  # 'farmer', 'elder', 'buyer'
    location: String,
    created_at: DateTime
}
"""

def create_user(mongo, username, email, password, user_type, location=None):
    """Create a new user document"""
    user = {
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password),
        'user_type': user_type,
        'location': location,
        'created_at': datetime.utcnow()
    }
    return mongo.db.users.insert_one(user)

def get_user_by_email(mongo, email):
    """Get user by email"""
    return mongo.db.users.find_one({'email': email})

def get_user_by_username(mongo, username):
    """Get user by username"""
    return mongo.db.users.find_one({'username': username})

def get_user_by_id(mongo, user_id):
    """Get user by ID"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return mongo.db.users.find_one({'_id': user_id})

def check_password(user, password):
    """Check password against stored hash"""
    return check_password_hash(user['password_hash'], password)

def user_to_dict(user):
    """Convert user document to dictionary for API responses"""
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'user_type': user['user_type'],
        'location': user['location'],
        'created_at': user['created_at'].isoformat()
    }