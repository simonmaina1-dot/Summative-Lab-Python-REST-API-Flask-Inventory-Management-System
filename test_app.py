import pytest
from app import app
from api_utils import fetch_product
import json
from unittest.mock import Mock
from models import InventoryItem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_inventory():
    from app import inventory
    inventory.clear()
    inventory.append(InventoryItem(product_name="Test Seed", id="test1"))

def test_get_inventory(client):
    rv = client.get('/inventory')
    assert rv.status_code == 200
    assert len(rv.json) == 1  # fixture seed
    assert rv.json[0]['product_name'] == 'Test Seed'

def test_add_item(client, monkeypatch):
    monkeypatch.setattr('api_utils.fetch_product', lambda query: None)
    rv = client.post('/inventory', json={'product_name': 'Test Item', 'stock': 10, 'price': 5.99})
    assert rv.status_code == 201
    data = rv.json
    assert data['product_name'] == 'Test Item'
    assert data['stock'] == 10
    assert 'id' in data

def test_get_item(client):
    rv = client.get('/inventory/test1')
    assert rv.status_code == 200
    assert rv.json['product_name'] == 'Test Seed'

def test_update_item(client):
    rv = client.patch('/inventory/test1', json={'stock': 20, 'price': 4.99})
    assert rv.status_code == 200
    assert rv.json['stock'] == 20

def test_delete_item(client):
    rv = client.delete('/inventory/test1')
    assert rv.status_code == 200
    rv2 = client.get('/inventory')
    assert len(rv2.json) == 0

def test_add_invalid(client):
    rv = client.post('/inventory', json={'stock': 10})
    assert rv.status_code == 400
    assert 'product_name required' in rv.json['error']

def test_lookup_api(client, monkeypatch):
    def mock_fetch(q):
        return {'product_name': 'Mock Product'}
    monkeypatch.setattr('api_utils.fetch_product', mock_fetch)
    rv = client.get('/lookup/mockquery')
    assert rv.status_code == 200
    assert rv.json['product_name'] == 'Mock Product'

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json['status'] == 'healthy'

def test_web_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Inventory Management' in rv.data

