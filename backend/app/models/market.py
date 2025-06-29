from app import db
from datetime import datetime

class MarketListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # 'kg', 'bags', 'bundles'
    price_per_unit = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'quantity': self.quantity,
            'unit': self.unit,
            'price_per_unit': self.price_per_unit,
            'location': self.location,
            'description': self.description,
            'farmer': self.farmer.username,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat()
        }