import json
import pytest

def test_user_registration(client):
    response = client.post('/api/auth/register', 
        json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'user_type': 'farmer'
        })
    
    data = response.json
    assert response.status_code == 201
    assert data['message'] == 'User registered successfully'

def test_user_login(client, sample_user):
    response = client.post('/api/auth/login',
        json={
            'username': 'testuser',
            'password': 'testpassword'
        })
    
    data = response.json
    assert response.status_code == 200
    assert 'access_token' in data
    assert data['user']['username'] == 'testuser'

def test_create_knowledge_entry(client, auth_headers):
    response = client.post('/api/knowledge/',
        json={
            'title': 'Cassava Processing',
            'content': 'How to process cassava into flour',
            'crop_type': 'Cassava',
            'season': 'Rainy Season',
            'region': 'Bong County',
            'language': 'English'
        },
        headers=auth_headers)
    
    data = response.json
    # This improved assertion will show the API error message if the status code is wrong
    assert response.status_code == 201, f"Expected status 201, but got {response.status_code}. Response: {data}"
    assert data['title'] == 'Cassava Processing'

def test_get_market_listings(client):
    response = client.get('/api/market/')
    data = response.json
    assert response.status_code == 200
    assert isinstance(data, list)