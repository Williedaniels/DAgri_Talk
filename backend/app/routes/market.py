from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy.exc import IntegrityError
from app.models.market import MarketListing

market_bp = Blueprint('market', __name__)

@market_bp.route('/', methods=['GET'])
def get_market_listings():
    try:
        listings = MarketListing.query.filter_by(is_available=True).all()
        return jsonify([listing.to_dict() for listing in listings]), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get market listings', 'error': str(e)}), 500

@market_bp.route('/', methods=['POST'])
@jwt_required()
def create_market_listing():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    if not data or not all(k in data for k in ['crop_name', 'quantity', 'unit', 'price_per_unit', 'location']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        listing = MarketListing(
            crop_name=data['crop_name'],
            quantity=float(data['quantity']),
            unit=data['unit'],
            price_per_unit=float(data['price_per_unit']),
            location=data['location'],
            description=data.get('description', ''),
            farmer_id=user_id
        )
        db.session.add(listing)
        db.session.commit()
        return jsonify(listing.to_dict()), 201
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid data type for quantity or price_per_unit. Must be a number.'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Database error, possible duplicate or invalid foreign key.'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create market listing', 'error': str(e)}), 500