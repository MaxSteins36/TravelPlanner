import pytest
from unittest.mock import patch, MagicMock
from login_DB import login_database_blueprint, check_user_exists, add_user_to_database
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(login_database_blueprint)
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def mock_dispatcher():
    with patch('database.dispatcher') as mock:
        yield mock

def test_check_user_exists(mock_dispatcher):
    mock_dispatcher.execute.return_value = [(1, 'test_user', 'test_password')]

    assert check_user_exists('test_user', 'test_password') is True
    mock_dispatcher.execute.assert_called_with("SELECT * FROM user_data WHERE username = %s AND password = %s", ('test_user', 'test_password'))

def test_check_user_not_exists(mock_dispatcher):
    mock_dispatcher.execute.return_value = []

    assert check_user_exists('non_existent_user', 'wrong_password') is False
    mock_dispatcher.execute.assert_called_with("SELECT * FROM user_data WHERE username = %s AND password = %s",
                                               ('non_existent_user', 'wrong_password'))
def test_add_user_to_database(mock_dispatcher):
    mock_dispatcher.execute.return_value = 1

    success = add_user_to_database('John', 'Doe', 'john_doe', 'password123', 'user_data')
    assert success is True
    mock_dispatcher.execute.assert_called_with("INSERT INTO user_data (username,first_name, last_name, password) VALUES (%s, %s, %s, %s)", ('john_doe', 'John', 'Doe', 'password123'))

def test_login_user_success(client, mock_dispatcher):
    mock_dispatcher.execute.return_value = [(1, 'test_user', 'test_password')]

    response = client.post('/login_user', json={'username': 'test_user', 'password': 'test_password'})
    assert response.status_code == 200
    assert response.json == {'success': True}

def test_add_user_success(client, mock_dispatcher):
    mock_dispatcher.execute.return_value = [(1,'Berry','Connell', 'jock12' , 'test_password')]

    response = client.post('/add_user', json={'first_name': 'Berry', 'last_name': 'Connel', 'username': 'jock12', 'password': 'test_password'})
    assert response.status_code == 200
    assert response.json == {'success': True}
