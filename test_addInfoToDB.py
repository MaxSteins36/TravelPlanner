import pytest
from unittest.mock import MagicMock
from addInfoToDB import add_trip_blueprint
from flask import Flask
from user import User


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(add_trip_blueprint)
    return app


@pytest.fixture
def mock_dispatcher():
    mock = MagicMock()
    mock.execute = MagicMock()
    mock.connection.commit = MagicMock()
    return mock


@pytest.fixture
def mock_user():
    mock = MagicMock()
    mock.id = 1
    return mock


def test_add_hotel_success(app, mock_dispatcher, mock_user):
    User.get_current_user = MagicMock(return_value=mock_user)
    
    with app.test_client() as client:
        data = {
            "name": "Hotel California",
            "room_type": "Suite",
            "bed_type": "King",
            "number_of_beds": 2,
            "price": 200.0
        }
        response = client.post('/add_hotel', json=data)
        
        mock_dispatcher.execute.assert_called_once()
        mock_dispatcher.connection.commit.assert_called_once()
        
        assert response.status_code == 200
        assert response.json == {"message": "Hotel added successfully!"}


def test_add_hotel_missing_name(app, mock_dispatcher, mock_user):
    User.get_current_user = MagicMock(return_value=mock_user)

    with app.test_client() as client:
        data = {
            "room_type": "Suite",
            "bed_type": "King",
            "number_of_beds": 2,
            "price": 200.0
        }
        response = client.post('/add_hotel', json=data)
        
        assert response.status_code == 400
        assert response.json == {"error": "Invalid data, 'name' key is missing"}


def test_add_trip_success(app, mock_dispatcher, mock_user):
    User.get_current_user = MagicMock(return_value=mock_user)
    
    with app.test_client() as client:
        data = {
            "flights": [
                {
                    "outbound": [
                        {
                            "price": 100.0,
                            "currency": "USD",
                            "number_of_seats": 100,
                            "departure": "JFK",
                            "arrival": "LAX",
                            "departure_time": "2024-12-01T12:00:00",
                            "arrival_time": "2024-12-01T15:00:00"
                        }
                    ],
                    "return": [
                        {
                            "price": 110.0,
                            "currency": "USD",
                            "number_of_seats": 50,
                            "departure": "LAX",
                            "arrival": "JFK",
                            "departure_time": "2024-12-02T10:00:00",
                            "arrival_time": "2024-12-02T13:00:00"
                        }
                    ]
                }
            ]
        }
        response = client.post('/add_trip', json=data)
        
        mock_dispatcher.execute.assert_called()
        mock_dispatcher.connection.commit.assert_called()
        
        assert response.status_code == 200
        assert response.json == {"message": "Trips and segments added successfully!"}


def test_add_trip_missing_flights(app, mock_dispatcher, mock_user):
    User.get_current_user = MagicMock(return_value=mock_user)
    
    with app.test_client() as client:
        data = {
            "hotels": [
                {
                    "name": "Hotel California",
                    "room_type": "Suite",
                    "bed_type": "King",
                    "number_of_beds": 2,
                    "price": 200.0
                }
            ]
        }
        response = client.post('/add_trip', json=data)
        
        assert response.status_code == 400
        assert response.json == {"error": "Invalid data, 'flights' key is missing"}
