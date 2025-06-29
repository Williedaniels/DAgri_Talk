import json
import pytest
from flask_jwt_extended import create_access_token

def test_user_registration(client):
    response = client.post('/api/auth/register', 
        json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'user_type': 'farmer'
        })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'User registered successfully'

def test_user_login(client, sample_user):
    response = client.post('/api/auth/login',
        json={
            'username': 'testuser',
            'password': 'testpassword'
        })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == 'testuser'

def test_create_knowledge_entry(client, sample_user, app):
    with app.app_context():
        access_token = create_access_token(identity=sample_user.id)
    
    response = client.post('/api/knowledge/',
        json={
            'title': 'Cassava Processing',
            'content': 'How to process cassava into flour',
            'crop_type': 'Cassava'
        },
        headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Cassava Processing'

def test_get_market_listings(client):
    response = client.get('/api/market/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)