import pytest
from unittest.mock import patch, MagicMock
from Flights import FlightSearch


@pytest.fixture
def flight_search():
    return FlightSearch()


@patch("Flights.FlightSearch.generate_access_token")
@patch("Flights.FlightSearch.get_iata_code")
@patch("Flights.requests.get")
def test_search_flights(mock_get, mock_get_iata_code, mock_generate_access_token, flight_search):
    mock_generate_access_token.return_value = None
    flight_search.access_token = "mocked_token"

    mock_get_iata_code.side_effect = lambda city: {"Los Angeles": "LAX", "New York": "JFK"}.get(city)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "price": {"total": "300.00", "currency": "USD"},
                "itineraries": [
                    {
                        "segments": [
                            {
                                "departure": {"iataCode": "LAX", "at": "2024-12-10T10:00"},
                                "arrival": {"iataCode": "JFK", "at": "2024-12-10T18:00"}
                            }
                        ]
                    },
                    {
                        "segments": [
                            {
                                "departure": {"iataCode": "JFK", "at": "2024-12-15T12:00"},
                                "arrival": {"iataCode": "LAX", "at": "2024-12-15T16:00"}
                            }
                        ]
                    }
                ],
                "numberOfBookableSeats": 5
            }
        ]
    }
    mock_get.return_value = mock_response

    results = flight_search.search_flights("Los Angeles", "New York", "2024-12-10", 1, "2024-12-15")

    assert len(results) == 1
    assert results[0]["price"] == "300.00"
    assert results[0]["currency"] == "USD"
    assert results[0]["number_of_seats"] == 5
    assert results[0]["outbound"] == [
        {
            "departure": "LAX",
            "arrival": "JFK",
            "departure_time": "2024-12-10T10:00",
            "arrival_time": "2024-12-10T18:00"
        }
    ]
    assert results[0]["return"] == [
        {
            "departure": "JFK",
            "arrival": "LAX",
            "departure_time": "2024-12-15T12:00",
            "arrival_time": "2024-12-15T16:00"
        }
    ]

    mock_get.assert_called_once_with(
        "https://test.api.amadeus.com/v2/shopping/flight-offers",
        headers={"Authorization": "Bearer mocked_token"},
        params={
            "originLocationCode": "LAX",
            "destinationLocationCode": "JFK",
            "departureDate": "2024-12-10",
            "adults": 1,
            "max": 10,
            "nonStop": "false",
            "returnDate": "2024-12-15"
        }
    )
