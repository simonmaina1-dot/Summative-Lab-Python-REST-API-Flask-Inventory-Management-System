import pytest
import sys
from unittest.mock import patch
from click.testing import CliRunner
from cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_list(runner):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = [{'product_name': 'Test Item'}]
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        assert 'Test Item' in result.stdout

def test_view(runner):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'product_name': 'View Item'}
        result = runner.invoke(cli, ['view', '123'])
        assert result.exit_code == 0

def test_add(runner):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'id': 'newid'}
        result = runner.invoke(cli, ['add', '--name', 'New', '--stock', '5', '--price', '1.99'])
        assert result.exit_code == 0

def test_update(runner):
    with patch('requests.patch') as mock_patch:
        mock_patch.return_value.json.return_value = {'stock': 10}
        result = runner.invoke(cli, ['update', '123', '--stock', '10'])
        assert result.exit_code == 0

def test_delete(runner):
    with patch('requests.delete') as mock_del:
        mock_del.return_value.json.return_value = {'message': 'deleted'}
        result = runner.invoke(cli, ['delete', '123'])
        assert result.exit_code == 0

def test_lookup(runner, monkeypatch):
    def mock_fetch(query):
        return {'product_name': 'API Test'}
    monkeypatch.setattr('cli.fetch_product', mock_fetch)
    result = runner.invoke(cli, ['lookup', 'barcode'])
    assert result.exit_code == 0
    assert 'API Test' in result.stdout

