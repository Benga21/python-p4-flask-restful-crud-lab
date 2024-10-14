import json
import pytest
from app import app, db, Plant

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.app_context():
        db.create_all()  # Create all tables
        # Add test data
        test_plant = Plant(name="Test Plant", image="test_image.jpg", price=10.00, is_in_stock=True)
        db.session.add(test_plant)
        db.session.commit()
        yield app.test_client()
        db.drop_all()  # Clean up after tests

def test_plant_by_id_get_route(client):
    response = client.get('/plants/1')
    assert response.status_code == 200

def test_plant_by_id_get_route_returns_one_plant(client):
    response = client.get('/plants/1')
    data = json.loads(response.data.decode())
    assert type(data) == dict
    assert data["id"]
    assert data["name"]

def test_plant_by_id_patch_route_updates_is_in_stock(client):
    response = client.patch(
        '/plants/1',
        json={"is_in_stock": False}
    )
    data = json.loads(response.data.decode())
    assert type(data) == dict
    assert data["id"]
    assert data["is_in_stock"] is False

def test_plant_by_id_delete_route_deletes_plant(client):
    response = client.delete('/plants/1')
    assert response.status_code == 204  # No content returned after deletion
