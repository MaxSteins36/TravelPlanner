import pytest
from unittest.mock import patch
import requests
from places_API import get_places_nearby, search_places, get_places_details, get_photo

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GGMAP_PLACES_API_KEY")


mock_location = "33.9720577784,-117.325408698"  # UCR Coordinates
mock_radius = 16000 #10 miles
mock_place_type = "university"

# 1. Test get_places_nearby()
#Test run sucessfully
@patch('requests.get')
def test_get_places_nearby(mock_get):
    mock_response = {
        "status": "OK",
        "results": [
            {
                "name": "University of California, Riverside",
                "geometry": {"location": {"lat": 33.9720577784, "lng": -117.325408698}},
                "formatted_address": "900 University Ave, Riverside, CA 92521, United States"
            }
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    places = get_places_nearby(mock_location, mock_radius, mock_place_type)

    assert len(places) == 1
    assert places[0]['name'] == "University of California, Riverside"
    assert places[0]['formatted_address'] == "900 University Ave, Riverside, CA 92521, United States"

# Test no result
@patch('requests.get')
def test_get_places_nearby_no_results(mock_get):
    mock_response = {
        "status": "OK",
        "results": []
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    places = get_places_nearby(mock_location, mock_radius, mock_place_type)

    assert places == []

# Test invalid API key (HTTP 403 - Forbidden)
@patch('requests.get')
def test_get_places_nearby_invalid_api_key(mock_get):
    mock_response = {
        "status": "REQUEST_DENIED"
    }
    mock_get.return_value.status_code = 403
    mock_get.return_value.json.return_value = mock_response

    places = get_places_nearby(mock_location, mock_radius, mock_place_type)

    assert places == []

# Test: Server Error (500)
@patch('requests.get')
def test_get_places_nearby_server_error(mock_get):
    mock_response = {
        "status": "ERROR"
    }
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = mock_response

    places = get_places_nearby(mock_location, mock_radius, mock_place_type)

    assert places == []

# 2. Test get_photo()
mock_photo_reference = "This_is_a_photo_reference"

# Test successfully run
@patch('requests.get')
def test_get_photo_success(mock_get):
    mock_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={mock_photo_reference}&key={API_KEY}"

    mock_get.return_value.status_code = 200
    mock_get.return_value.url = mock_url

    photo_url = get_photo(mock_photo_reference)

    assert photo_url == mock_url

# Test invalid photo reference
@patch('requests.get')
def test_get_photo_invalid_reference(mock_get):

    # Error code 400
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {'status': 'INVALID_REQUEST'}

    photo_url = get_photo(mock_photo_reference)

    assert photo_url == 'N/A'

# Test exceptions
@patch('requests.get')
def test_get_photo_request_exception(mock_get):

    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

    photo_url = get_photo(mock_photo_reference)

    assert photo_url == 'N/A'

# 3. Test serach_places()
mock_query = "stadium in Riverside"
# Test run successfully
@patch('requests.get')
def test_search_places_success(mock_get):

    mock_response = {
        "status": "OK",
        "results": [
            {
                "name": "Riverside Stadium",
                "formatted_address": "123 Riverside Blvd, Riverside, CA",
                "geometry": {
                    "location": {"lat": 33.9800, "lng": -117.3750}
                }
            },
            {
                "name": "Riverside Sports Arena",
                "formatted_address": "456 Riverside Ave, Riverside, CA",
                "geometry": {
                    "location": {"lat": 33.9810, "lng": -117.3760}
                }
            }
        ]
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    places = search_places(mock_query)

    assert len(places) == 2
    assert places[0]['name'] == "Riverside Stadium"
    assert places[1]['address'] == "456 Riverside Ave, Riverside, CA"

# Test invalid API key
@patch('requests.get')
def test_search_places_invalid_api_key(mock_get):

    mock_response = {
        "status": "REQUEST_DENIED"
    }

    mock_get.return_value.status_code = 403
    mock_get.return_value.json.return_value = mock_response

    places = search_places(mock_query)

    assert places == []

# Test Server Error
@patch('requests.get')
def test_search_places_server_error(mock_get):

    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'status': 'ERROR'}

    places = search_places(mock_query)

    assert places == []

# 4. Test get_places_details()
mock_place_id = "Place_ID_for_testing"

# Test Successfully run
@patch('requests.get')
def test_get_places_details_success(mock_get):
    mock_response = {
        "status": "OK",
        "result": {
            "name": "University of California, Riverside",
            "formatted_address": "900 University Ave, Riverside, CA 92521",
            "geometry": {
                "location": {"lat": 33.972057, "lng": -117.325408}
            }
        }
    }
    
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    place_details = get_places_details(mock_place_id)

    assert place_details['name'] == "University of California, Riverside"
    assert place_details['formatted_address'] == "900 University Ave, Riverside, CA 92521"
    assert place_details['geometry']['location']['lat'] == 33.972057

# Test Error response
@patch('requests.get')
def test_get_places_details_error(mock_get):

    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"status": "REQUEST_DENIED"}

    place_details = get_places_details(mock_place_id)

    assert place_details == {}

# Test Server Error
@patch('requests.get')
def test_get_places_details_server_error(mock_get):

    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {'status': 'ERROR'}

    place_details = get_places_details(mock_place_id)

    assert place_details == {}

# Running the tests
if __name__ == "__main__":
    pytest.main()