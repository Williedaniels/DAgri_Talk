from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

market_bp = Blueprint('market', __name__)

@market_bp.route('/', methods=['GET'])
def get_market_listings():
    try:
        available_only = request.args.get('available_only', 'true').lower() == 'true'
        
        db = get_db()
        query = {'is_available': True} if available_only else {}
        listings = list(db.market_listings.find(query))
        
        # Convert ObjectId to string for JSON serialization
        for listing in listings:
            listing['_id'] = str(listing['_id'])
            if 'farmer_id' in listing and listing['farmer_id']:
                listing['farmer_id'] = str(listing['farmer_id'])
            
            # Format dates for JSON serialization
            if 'created_at' in listing:
                listing['created_at'] = listing['created_at'].isoformat()
            if 'updated_at' in listing:
                listing['updated_at'] = listing['updated_at'].isoformat()
                
            # Add farmer username if possible
            if 'farmer_id' in listing and listing['farmer_id']:
                farmer = db.users.find_one({'_id': ObjectId(listing['farmer_id'])})
                listing['farmer_username'] = farmer['username'] if farmer else 'Unknown'
        
        return jsonify(listings), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching market listings: {str(e)}")
        return jsonify({'message': 'Error fetching market listings', 'error': str(e)}), 500

@market_bp.route('/', methods=['POST'])
@jwt_required()
def create_market_listing():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or not all(k in data for k in ['crop_name', 'quantity', 'unit', 'price_per_unit', 'location']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        now = datetime.utcnow()
        new_listing = {
            'crop_name': data['crop_name'],
            'quantity': float(data['quantity']),
            'unit': data['unit'],
            'price_per_unit': float(data['price_per_unit']),
            'location': data['location'],
            'description': data.get('description', ''),
            'farmer_id': ObjectId(user_id) if user_id else None,
            'is_available': True,
            'created_at': now,
            'updated_at': now
        }
        
        db = get_db()
        result = db.market_listings.insert_one(new_listing)
        
        # Get the newly created listing
        listing = db.market_listings.find_one({'_id': result.inserted_id})
        
        # Prepare response
        listing['_id'] = str(listing['_id'])
        if 'farmer_id' in listing and listing['farmer_id']:
            listing['farmer_id'] = str(listing['farmer_id'])
        if 'created_at' in listing:
            listing['created_at'] = listing['created_at'].isoformat()
        if 'updated_at' in listing:
            listing['updated_at'] = listing['updated_at'].isoformat()
        
        # Add farmer username
        farmer = db.users.find_one({'_id': ObjectId(user_id)}) if user_id else None
        listing['farmer_username'] = farmer['username'] if farmer else 'Unknown'
        
        return jsonify(listing), 201
    except ValueError:
        return jsonify({'message': 'Invalid data type for quantity or price_per_unit. Must be a number.'}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating market listing: {str(e)}")
        return jsonify({'message': 'Failed to create market listing', 'error': str(e)}), 500