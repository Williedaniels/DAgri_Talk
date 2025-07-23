from datetime import datetime
from bson.objectid import ObjectId

def create_market_listing(mongo, crop_name, quantity, unit, price_per_unit, 
                        location, farmer_id, description=None):
    """Create a new market listing document"""
    now = datetime.utcnow()
    listing = {
        'crop_name': crop_name,
        'quantity': float(quantity),
        'unit': unit,
        'price_per_unit': float(price_per_unit),
        'location': location,
        'description': description,
        'farmer_id': ObjectId(farmer_id),
        'is_available': True,
        'created_at': now,
        'updated_at': now
    }
    return mongo.db.market_listings.insert_one(listing)

def get_market_listing(mongo, listing_id):
    """Get market listing by ID"""
    if isinstance(listing_id, str):
        listing_id = ObjectId(listing_id)
    return mongo.db.market_listings.find_one({'_id': listing_id})

def get_all_market_listings(mongo, available_only=True):
    """Get all market listings, optionally filtering for only available ones"""
    query = {'is_available': True} if available_only else {}
    return list(mongo.db.market_listings.find(query))

def market_listing_to_dict(mongo, listing):
    """Convert market listing to dictionary for API responses"""
    farmer = mongo.db.users.find_one({'_id': listing['farmer_id']})
    farmer_username = farmer['username'] if farmer else None
    
    return {
        'id': str(listing['_id']),
        'crop_name': listing['crop_name'],
        'quantity': listing['quantity'],
        'unit': listing['unit'],
        'price_per_unit': listing['price_per_unit'],
        'location': listing['location'],
        'description': listing.get('description', ''),
        'farmer_id': str(listing['farmer_id']),
        'farmer_username': farmer_username,
        'is_available': listing['is_available'],
        'created_at': listing['created_at'].isoformat(),
        'updated_at': listing['updated_at'].isoformat()
    }