import pytest
import sys
from unittest.mock import patch, Mock
from io import StringIO
from contextlib import redirect_stdout
import cli  # Import to access functions for testing

def test_list(capsys):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = [{'product_name': 'Test Item'}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        sys.argv = ['cli.py', 'list']
        cli.main()
        
        captured = capsys.readouterr()
        assert 'Test Item' in captured.out
        assert captured.err == ''


def test_view(capsys):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'product_name': 'View Item'}
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        sys.argv = ['cli.py', 'view', '123']
        cli.main()
        
        captured = capsys.readouterr()
        assert 'View Item' in captured.out
        assert captured.err == ''


def test_add(capsys):
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'newid'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        sys.argv = ['cli.py', 'add', '--name', 'New', '--stock', '5', '--price', '1.99']
        cli.main()
        
        captured = capsys.readouterr()
        assert '"id": "newid"' in captured.out


def test_update(capsys):
    with patch('requests.patch') as mock_patch:
        mock_response = Mock()
        mock_response.json.return_value = {'stock': 10}
        mock_response.raise_for_status.return_value = None
        mock_patch.return_value = mock_response
        
        sys.argv = ['cli.py', 'update', '123', '--stock', '10']
        cli.main()
        
        captured = capsys.readouterr()
        assert '"stock": 10' in captured.out


def test_delete(capsys):
    with patch('requests.delete') as mock_del:
        mock_response = Mock()
        mock_response.json.return_value = {'message': 'deleted'}
        mock_response.raise_for_status.return_value = None
        mock_del.return_value = mock_response
        
        sys.argv = ['cli.py', 'delete', '123']
        cli.main()
        
        captured = capsys.readouterr()
        assert '"message": "deleted"' in captured.out


def test_lookup(capsys, monkeypatch):
    def mock_fetch(query):
        return {'product_name': 'API Test'}
    
    monkeypatch.setattr('cli.fetch_product', mock_fetch)
    
    sys.argv = ['cli.py', 'lookup', 'barcode']
    cli.main()
    
    captured = capsys.readouterr()
    assert 'API Test' in captured.out
