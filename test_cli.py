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
        mock_get.return_value.json.return_value = []
        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0

def test_lookup(runner, mocker):
    mocker.patch('api_utils.fetch_product', return_value={'product_name': 'Test'})
    result = runner.invoke(cli, ['lookup', '123456'])
    assert result.exit_code == 0
    assert 'Test' in result.stdout

