import pytest
from unittest.mock import patch, MagicMock
from api_utils import fetch_product

@patch('requests.get')
def test_fetch_product_barcode(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 1,
        'product': {'product_name': 'Test Product'}
    }
    mock_get.return_value = mock_response
    
    result = fetch_product('123456789')
    assert result is not None
    assert result['product_name'] == 'Test Product'

@patch('requests.get')
def test_fetch_product_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    result = fetch_product('invalid')
    assert result is None

