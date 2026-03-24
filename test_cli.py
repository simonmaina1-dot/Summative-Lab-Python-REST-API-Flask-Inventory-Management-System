import pytest
from unittest.mock import patch, Mock, call
import cli
from io import StringIO

@patch('cli.requests')
def test_do_list(mock_requests, capsys):
    mock_response = Mock()
    mock_response.json.return_value = [{'product_name': 'Test Item'}]
    mock_response.raise_for_status.return_value = None
    mock_requests.get.return_value = mock_response
    
    args = type('Args', (), {'command': None})()
    cli.do_list(args)
    
    captured = capsys.readouterr()
    assert 'Test Item' in captured.out
    mock_requests.get.assert_called_once_with('http://127.0.0.1:5000/inventory')

@patch('cli.requests')
def test_do_view(mock_requests, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {'product_name': 'View Item'}
    mock_response.raise_for_status.return_value = None
    mock_requests.get.return_value = mock_response
    
    args = type('Args', (), {'item_id': '123'})()
    cli.do_view(args)
    
    captured = capsys.readouterr()
    assert 'View Item' in captured.out
    mock_requests.get.assert_called_once_with('http://127.0.0.1:5000/inventory/123')

@patch('cli.requests')
def test_do_add(mock_requests, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {'id': 'newid'}
    mock_response.raise_for_status.return_value = None
    mock_requests.post.return_value = mock_response
    
    args = type('Args', (), {'name': 'New Item', 'price': 1.99, 'stock': 5, 'barcode': None})()
    cli.do_add(args)
    
    captured = capsys.readouterr()
    assert '"id": "newid"' in captured.out
    mock_requests.post.assert_called_once()

@patch('cli.requests')
def test_do_update(mock_requests, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {'stock': 10}
    mock_response.raise_for_status.return_value = None
    mock_requests.patch.return_value = mock_response
    
    args = type('Args', (), {'item_id': '123', 'price': None, 'stock': 10})()
    cli.do_update(args)
    
    captured = capsys.readouterr()
    assert '"stock": 10' in captured.out
    mock_requests.patch.assert_called_once_with('http://127.0.0.1:5000/inventory/123', json={'stock': 10})

@patch('cli.requests')
def test_do_delete(mock_requests, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {'message': 'deleted'}
    mock_response.raise_for_status.return_value = None
    mock_requests.delete.return_value = mock_response
    
    args = type('Args', (), {'item_id': '123'})()
    cli.do_delete(args)
    
    captured = capsys.readouterr()
    assert '"message": "deleted"' in captured.out
    mock_requests.delete.assert_called_once_with('http://127.0.0.1:5000/inventory/123')

@patch('cli.fetch_product')
def test_do_lookup(mock_fetch, capsys):
    mock_fetch.return_value = {'product_name': 'API Test'}
    args = type('Args', (), {'barcode': 'testbc'})()
    cli.do_lookup(args)
    
    captured = capsys.readouterr()
    assert 'API Test' in captured.out

@patch('cli.input')
@patch('cli.requests')
def test_interactive_menu(mock_requests, mock_input, capsys):
    # Mock input sequence: choice 0 (quit)
    mock_input.side_effect = ['0']
    
    # Quick test: run menu, expect no API calls, quit message
    cli.interactive_menu()
    
    captured = capsys.readouterr()
    assert 'Goodbye!' in captured.out
    mock_input.assert_called()

