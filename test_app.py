import pytest
import threading
import time
from app import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route returns correct message."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Todo API is running!" in response.data

def test_get_todos_empty(client):
    """Test getting todos when list is empty."""
    response = client.get('/todos')
    assert response.status_code == 200

def test_add_todo(client):
    """Test adding a new todo."""
    response = client.post('/todos',
        json={'task': 'Test task'},
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['task'] == 'Test task'
    assert data['done'] == False
