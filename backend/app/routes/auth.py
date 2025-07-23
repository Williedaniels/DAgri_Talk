from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app.database import get_db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# Helper functions for user operations
def get_user_by_email(email):
    db = get_db()
    return db.users.find_one({'email': email})

def get_user_by_username(username):
    db = get_db()
    return db.users.find_one({'username': username})

def get_user_by_id(user_id):
    db = get_db()
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return db.users.find_one({'_id': user_id})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if get_user_by_email(data['email']):
        return jsonify({'message': 'Email already exists'}), 409
    
    if get_user_by_username(data['username']):
        return jsonify({'message': 'Username already exists'}), 409
    
    # Create new user
    hashed_password = generate_password_hash(data['password'])
    user = {
        'username': data['username'],
        'email': data['email'],
        'password_hash': hashed_password,
        'user_type': data.get('user_type', 'farmer'),
        'location': data.get('location'),
        'created_at': datetime.utcnow()
    }
    
    db = get_db()
    result = db.users.insert_one(user)
    
    return jsonify({'message': 'User registered successfully', 'user_id': str(result.inserted_id)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    user = None
    # Try to find user by username or email
    if 'username' in data:
        user = get_user_by_username(data['username'])
    elif 'email' in data:
        user = get_user_by_email(data['email'])
    else:
        return jsonify({'message': 'Missing username or email'}), 400
    
    # Verify password
    if not user or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Create access token
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        'access_token': access_token,
        'user_id': str(user['_id']),
        'username': user['username']
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Remove sensitive fields
    user_data = {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'user_type': user.get('user_type', 'user'),
        'location': user.get('location'),
        'created_at': user['created_at']
    }
    
    return jsonify(user_data), 200