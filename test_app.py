import pytest
from app import app
from models import InventoryItem
from api_utils import fetch_product
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    rv = client.get('/inventory')
    assert rv.status_code == 200
    assert rv.json == []

def test_add_item(client, mocker):
    mocker.patch('api_utils.fetch_product', return_value=None)
    rv = client.post('/inventory', json={'product_name': 'Test Item', 'stock': 10, 'price': 5.99})
    assert rv.status_code == 201
    data = rv.json
    assert data['product_name'] == 'Test Item'

def test_get_item_not_found(client):
    rv = client.get('/inventory/nonexistent')
    assert rv.status_code == 404

def test_delete_nonexistent(client):
    rv = client.delete('/inventory/nonexistent')
    assert rv.status_code == 404

