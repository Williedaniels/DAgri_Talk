import pytest
from app import create_app
from app.extensions import mongo
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson.objectid import ObjectId

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        # Clear the test database
        mongo.db.users.delete_many({})
        mongo.db.knowledge_entries.delete_many({})
        mongo.db.market_listings.delete_many({})
        yield app
        # Clean up after tests
        mongo.db.users.delete_many({})
        mongo.db.knowledge_entries.delete_many({})
        mongo.db.market_listings.delete_many({})

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': generate_password_hash('testpassword'),
            'user_type': 'farmer',
            'location': 'Monrovia',
            'created_at': datetime.utcnow()
        }
        user_id = mongo.db.users.insert_one(user).inserted_id
        user['_id'] = user_id
        return user

@pytest.fixture
def auth_headers(app, sample_user):
    """
    Fixture that creates an access token for the sample_user
    and returns a dictionary with the correct Authorization header.
    """
    with app.app_context():
        # The identity must be a string to avoid serialization issues with ObjectId
        access_token = create_access_token(identity=str(sample_user['_id']))
    headers = {'Authorization': f'Bearer {access_token}'}
    return headers