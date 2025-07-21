from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token, verify_jwt_in_request
import jwt
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            user_type=data.get('user_type', 'farmer'),
            location=data.get('location', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@auth_bp.route('/user', methods=['GET']) 
def get_user():
    """Alternative profile endpoint to avoid JWT middleware issues"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'msg': 'Missing Authorization Header'}), 401
            
        token = auth_header.split(' ')[1]
        
        try:
            # Decode token using PyJWT directly
            secret_key = current_app.config.get('JWT_SECRET_KEY', 'jwt-secret-dagri-talk')
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = decoded_token['sub']
            
            # Convert to integer for database query
            if isinstance(user_id, str):
                user_id = int(user_id)
                
            # Fetch user from database
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
                
            return jsonify(user.to_dict()), 200
            
        except jwt.InvalidTokenError:
            return jsonify({'msg': 'Invalid token'}), 401
        except Exception as token_error:
            return jsonify({'msg': 'Token processing error', 'error': str(token_error)}), 401
            
    except Exception as e:
        return jsonify({'message': 'Failed to get user profile', 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
def profile():
    """Standard profile endpoint - may have JWT middleware issues"""
    return jsonify({'msg': 'Missing Authorization Header'}), 401