import pytest
from unittest.mock import patch, MagicMock
from Hotels import HotelSearch


@pytest.fixture
def hotel_search():
    return HotelSearch()


@patch("Hotels.requests.get")
def test_get_hotel_ids_by_city(mock_get, hotel_search):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {"hotelId": "86MDJK34"},
            {"hotelId": "92XPLT57"}
        ]
    }
    mock_get.return_value = mock_response
  
    hotel_ids = hotel_search.get_hotel_ids_by_city("DAL")
  
    assert hotel_ids == ["86MDJK34", "92XPLT57"]
    mock_get.assert_called_once_with(
        "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city",
        headers={"Authorization": f"Bearer {hotel_search.access_token}"},
        params={
            "cityCode": "DAL",
            "radius": 5,
            "radiusUnit": "KM",
            "hotelSource": "ALL"
        }
    )


@patch("Hotels.requests.get")
def test_get_hotel_offers(mock_get, hotel_search):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "hotel": {"name": "Mock Hotel"},
                "offers": [
                    {
                        "room": {
                            "typeEstimated": {
                                "category": "Deluxe",
                                "bedType": "King",
                                "beds": 1
                            }
                        },
                        "price": {"total": "150.00"}
                    }
                ]
            }
        ]
    }
    mock_get.return_value = mock_response

    results = hotel_search.get_hotel_offers(["86MDJK34"], "2024-12-10", "2024-12-12", 2, 1)

    # Assertions
    assert len(results) == 1
    assert results[0]["name"] == "Mock Hotel"
    assert results[0]["room_type"] == "Deluxe"
    assert results[0]["bed_type"] == "King"
    assert results[0]["price"] == "150.00"
    assert results[0]["number_of_beds"] == 1

    mock_get.assert_called_once_with(
        "https://test.api.amadeus.com/v3/shopping/hotel-offers",
        headers={"Authorization": f"Bearer {hotel_search.access_token}"},
        params={
            "hotelIds": "86MDJK34",
            "adults": 2,
            "checkInDate": "2024-12-10",
            "checkOutDate": "2024-12-12",
            "roomQuantity": 1,
            "paymentPolicy": "NONE",
            "bestRateOnly": "true"
        },
        timeout=30
    )


@patch("Hotels.HotelSearch.get_iata_code")
@patch("Hotels.HotelSearch.get_hotel_ids_by_city")
@patch("Hotels.HotelSearch.get_hotel_offers")
@patch("Hotels.HotelSearch.generate_access_token")
def test_search_hotels(mock_generate_access_token, mock_get_hotel_offers, mock_get_hotel_ids_by_city, mock_get_iata_code, hotel_search):
    mock_generate_access_token.return_value = None
    hotel_search.access_token = "mocked_token"

    mock_get_iata_code.return_value = "DAL"
    mock_get_hotel_ids_by_city.return_value = ["86MDJK34"]

    mock_get_hotel_offers.return_value = [
        {
            "name": "Mock Hotel",
            "room_type": "Deluxe",
            "bed_type": "King",
            "price": "150.00",
            "number_of_beds": 1
        }
    ]

    results = hotel_search.search_hotels("Dallas", "2024-12-10", "2024-12-12", 2, 1)

    assert results is None
    mock_get_iata_code.assert_called_once_with("Dallas")
    mock_get_hotel_ids_by_city.assert_called_once_with("DAL")
    mock_get_hotel_offers.assert_called_once_with(["86MDJK34"], "2024-12-10", "2024-12-12", 2, 1)
