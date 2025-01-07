import requests
from base import AmadeusBase

class HotelSearch(AmadeusBase):
    def search_hotels(self, city_name, check_in_date, check_out_date, adults, room_quantity=1):
        if not self.access_token:
            self.generate_access_token()

        city_iata_code = self.get_iata_code(city_name)
        if not city_iata_code:
            print(f"Error: Unable to find IATA code for city {city_name}.")
            return
        
        hotel_ids = self.get_hotel_ids_by_city(city_iata_code)
        if not hotel_ids:
            print(f"Error: No hotels found in city {city_name}.")
            return

        hotel_ids = hotel_ids[:10]

        hotel_offers = self.get_hotel_offers(hotel_ids, check_in_date, check_out_date, adults, room_quantity)
        print(f"Hotel Offers: {hotel_offers}")  # Debug statement to check the results
        return hotel_offers

    def get_hotel_ids_by_city(self, city_iata_code):
        url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
        params = {
            "cityCode": city_iata_code,  
            "radius": 5, 
            "radiusUnit": "KM", 
            "hotelSource": "ALL" 
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        print(f"Requesting hotel list for city: {city_iata_code}")
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            hotel_data = response.json().get("data", [])
            hotel_ids = [hotel["hotelId"] for hotel in hotel_data]  # Collect hotel IDs
            return hotel_ids
        else:
            print(f"Failed to retrieve hotel list: {response.status_code} {response.json()}")
            return []

    def get_hotel_offers(self, hotel_ids, check_in_date, check_out_date, adults, room_quantity):
        url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
        params = {
            "hotelIds": ",".join(hotel_ids),
            "adults": adults,
            "checkInDate": check_in_date,
            "checkOutDate": check_out_date,
            "roomQuantity": room_quantity,
            "paymentPolicy": "NONE",
            "bestRateOnly": "true"
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        print(f"Requesting hotel offers for hotel IDs: {', '.join(hotel_ids)}")
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []

        if response.status_code == 200:
            hotel_offers = response.json().get("data", [])
            results = []
            for offer in hotel_offers[:10]:
                hotel = offer["hotel"]

                try:
                    room_type = offer["offers"][0]["room"]["typeEstimated"]["category"]
                    bed_type = offer["offers"][0]["room"]["typeEstimated"]["bedType"]
                    price = offer["offers"][0]["price"]["total"]
                    number_of_beds = offer["offers"][0]["room"]["typeEstimated"].get("beds", "Not specified")
                except KeyError:
                    room_type = "Not Available"
                    bed_type = "Not Available"
                    price = "Not Available"
                    number_of_beds = "Not specified"

                results.append({
                    "name": hotel['name'],
                    "room_type": room_type,
                    "bed_type": bed_type,
                    "price": price,
                    "number_of_beds": number_of_beds
                })
            return results
        else:
            print(f"Failed to retrieve hotel offers: {response.status_code} {response.json()}")
