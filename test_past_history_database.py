import pytest
from flask import Flask, jsonify
from unittest.mock import patch, MagicMock
from user import User
from past_history_database import past_history_database

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(past_history_database)
    return app
@pytest.fixture
def client(app):
    return app.test_client()
@pytest.fixture
def mock_user():
    user_mock = MagicMock()
    user_mock.get_current_user.return_value = user_mock
    return user_mock
def test_past_history(client, mock_user):
    mock_user.get_flight_information.return_value = [
        {
            "flight_id": 1,
            "price": 200.0,
            "currency": "USD",
            "number_of_seats": 150,
            "segments": [{"type": "direct", "departure": "NYC", "arrival": "LA", "departure_time": "10:00", "arrival_time": "12:00"}]
        }
    ]
    mock_user.get_hotel_information.return_value = [
        {
            "hotel_id": 1,
            "hotel_name": "Hotel ABC",
            "check_in_date": "2023-12-01",
            "check_out_date": "2023-12-05",
            "location": "NYC",
            "price": 100.0,
            "currency": "USD"
        }
    ]
    response = client.get('/past_history')
    assert response.status_code == 200
    data = response.get_json()
    assert "past_flights" in data
    assert len(data["past_flights"]) > 0
    assert "past_hotels" in data
    assert len(data["past_hotels"]) > 0
def test_get_user_credentials(client, mock_user):
    mock_user.get_first_name.return_value = [{"first_name": "John"}]
    mock_user.get_last_name.return_value = [{"last_name": "Doe"}]
    response = client.get('/get_user_credentials')
    assert response.status_code == 200
    data = response.get_json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
def test_past_history_no_user(client):
    with patch.object(User, 'get_current_user', return_value=None):
        response = client.get('/past_history')
        assert response.status_code == 401
        data = response.get_json()
        assert data["error"] == "No user is currently logged in"
def test_get_user_credentials_no_user(client):
    with patch.object(User, 'get_current_user', return_value=None):
        response = client.get('/get_user_credentials')
        assert response.status_code == 401
        data = response.get_json()
        assert data["error"] == "No user is currently logged in"
def test_get_user_credentials_not_found(client, mock_user):
    mock_user.get_first_name.return_value = []
    mock_user.get_last_name.return_value = []
    response = client.get('/get_user_credentials')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "User credentials not found"