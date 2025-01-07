import requests
from base import AmadeusBase

class FlightSearch(AmadeusBase):
    def search_flights(self, origin, destination, departure_date, adults, return_date=None):
        if not self.access_token:
            self.generate_access_token()
            
        origin_iata_code = self.get_iata_code(origin)
        destination_iata_code = self.get_iata_code(destination)
        
        if not origin_iata_code or not destination_iata_code:
            print("Error: Unable to find IATA code for the cities.")
            return

        params = {
            "originLocationCode": origin_iata_code,
            "destinationLocationCode": destination_iata_code,
            "departureDate": departure_date,
            "adults": adults,
            "max": 10,  # Limit to 10 results for the search
            "nonStop": "false"  # Optional, change this if you need non-stop flights
        }

        if return_date:
            params["returnDate"] = return_date

        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        print(f"Requesting flight offers for {origin} to {destination}, Departure: {departure_date}")
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            flight_data = response.json().get("data", [])
            if not flight_data:
                print("No flight offers available for the given parameters.")
                return []
        
            results = []

            for offer in flight_data[:10]:
                price = offer["price"]["total"]
                currency = offer["price"]["currency"]
                flight_segments = offer["itineraries"][0]["segments"]
                number_of_seats = offer.get("numberOfBookableSeats", "Not specified")
                return_segments = offer["itineraries"][1]["segments"] if return_date else None

                outbound = [{"departure": s["departure"]["iataCode"], 
                             "arrival": s["arrival"]["iataCode"], 
                             "departure_time": s["departure"]["at"], 
                             "arrival_time": s["arrival"]["at"]} for s in flight_segments]
                
                return_segments = []
                if return_date:
                    return_segments = [{"departure": s["departure"]["iataCode"], 
                                        "arrival": s["arrival"]["iataCode"], 
                                        "departure_time": s["departure"]["at"], 
                                        "arrival_time": s["arrival"]["at"]} for s in offer["itineraries"][1]["segments"]]

                results.append({
                    "price": price,
                    "currency": currency,
                    "number_of_seats": number_of_seats,
                    "outbound": outbound,
                    "return": return_segments
                })

            return results
        else:
            print(f"Failed to retrieve flight offers: {response.status_code} {response.json()}")
