import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.utils.time_utils import hora_sistema


def test_hora_endpoint():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/hora')
        assert response.status_code == 200
        data = response.get_json()
        assert 'hora' in data


def test_hora_sistema():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {'hora': '2025-01-01 12:00:00.000000'}
    with patch('requests.get', return_value=mock_resp) as mock_get:
        data = hora_sistema()
        assert data == {'hora': '2025-01-01 12:00:00.000000'}
        mock_get.assert_called()
