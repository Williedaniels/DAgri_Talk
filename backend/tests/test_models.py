import pytest
from app.models.user import User
from app.models.knowledge import KnowledgeEntry
from app.models.market import MarketListing
from app import db

def test_user_creation_and_password(app):
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            user_type='farmer'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')

def test_knowledge_entry_creation(app, sample_user):
    with app.app_context():
        entry = KnowledgeEntry(
            title='Rice Farming Techniques',
            content='Traditional methods for growing rice in Liberia',
            crop_type='Rice',
            author_id=sample_user.id
        )
        db.session.add(entry)
        db.session.commit()
        
        assert entry.id is not None
        assert entry.title == 'Rice Farming Techniques'
        assert entry.author.username == 'testuser'

def test_market_listing_creation(app, sample_user):
    with app.app_context():
        listing = MarketListing(
            crop_name='Cassava',
            quantity=100.0,
            unit='kg',
            price_per_unit=50.0,
            location='Monrovia',
            farmer_id=sample_user.id
        )
        db.session.add(listing)
        db.session.commit()
        
        assert listing.id is not None
        assert listing.crop_name == 'Cassava'
        assert listing.farmer.username == 'testuser'