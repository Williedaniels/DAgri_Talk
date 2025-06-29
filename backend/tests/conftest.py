import pytest
from app import create_app, db
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