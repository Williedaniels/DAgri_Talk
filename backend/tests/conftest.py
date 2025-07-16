import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token
from app.models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_user(app):
    user = User(
        username='testuser',
        email='test@example.com',
        user_type='farmer',
        location='Monrovia'
    )
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def auth_headers(app, sample_user):
    """
    Fixture that creates an access token for the sample_user
    and returns a dictionary with the correct Authorization header.
    """
    with app.app_context():
        # The identity must be a string to avoid JWT errors
        access_token = create_access_token(identity=str(sample_user.id))
    headers = {'Authorization': f'Bearer {access_token}'}
    return headers