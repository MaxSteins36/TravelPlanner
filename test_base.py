import pytest
from unittest.mock import patch, MagicMock
from base import AmadeusBase

#Calling the real API would shift these from unit tests to integration tests. 
#Integration tests are also valuable but are used in different scenarios:

@pytest.fixture
def amadeus_base():
    return AmadeusBase()


@patch("base.requests.post")
def test_generate_access_token(mock_post, amadeus_base):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "mocked_token"}
    mock_post.return_value = mock_response

    amadeus_base.generate_access_token()

    assert amadeus_base.access_token == "mocked_token"
    mock_post.assert_called_once_with(
        "https://test.api.amadeus.com/v1/security/oauth2/token",
        data={
            'grant_type': 'client_credentials',
            'client_id': amadeus_base.api_key,
            'client_secret': amadeus_base.api_secret,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )


@patch("base.requests.get")
def test_get_iata_code(mock_get, amadeus_base):
    amadeus_base.access_token = "mocked_token"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [{"iataCode": "LAX"}]
    }
    mock_get.return_value = mock_response
    iata_code = amadeus_base.get_iata_code("Los Angeles")

    assert iata_code == "LAX"
    mock_get.assert_called_once_with(
        "https://test.api.amadeus.com/v1/reference-data/locations",
        headers={"Authorization": f"Bearer mocked_token"},
        params={"subType": "CITY", "keyword": "Los Angeles"}
    )
