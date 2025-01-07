import os
import requests
import dotenv

dotenv.load_dotenv()

class AmadeusBase:
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.access_token = None

    def generate_access_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret,
        }

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
        else:
            raise Exception("Failed to retrieve access token.")

    def get_iata_code(self, city_name):
        if not self.access_token:
            self.generate_access_token()

        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        params = {
            "subType": "CITY",
            "keyword": city_name
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0].get("iataCode")
            else:
                raise ValueError("IATA code not found for the given city.")
        else:
            raise Exception("Failed to retrieve IATA code.")
