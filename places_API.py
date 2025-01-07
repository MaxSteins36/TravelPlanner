import json

from dotenv import load_dotenv
import os
import requests
import urllib.parse

load_dotenv()
API_KEY = os.getenv("GGMAP_PLACES_API_KEY")

def get_places_nearby(location, radius, place_type):
	base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
	params = {
		'location': location,
		'radius': radius,
		'type': place_type,
		'key': API_KEY
	}
	url = f"{base_url}?{urllib.parse.urlencode(params)}"
	response = requests.get(url)

	try:
		if response.status_code == 200:
			data = response.json()
			return data.get('results', [])
		else:
			print(f"Error fetching data: {response.status}")
			return []

	except Exception as ex:
		print(f"An error occurred: {ex}")
		return []

def search_places(input):
	base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
	params = {
		'query': input,
		'key': API_KEY
		}
	url = f"{base_url}?{urllib.parse.urlencode(params)}"
	response = requests.get(url)

	try:
		if response.status_code == 200:
			data = response.json()
		
			if data['status'] == 'OK':
				places = []
				for result in data['results']:
					place = {
						'name': result['name'],
						'address': result.get('formatted_address', 'No address available'),
						'location': result['geometry']['location']
					}
					places.append(place)
				return places
			else:
				print("Error: No results found or invalid API key.")
				return None
		else:
                	print(f"Error fetching data: {response.status}")
                	return []

	except Exception as ex:
        	print(f"An error occurred: {ex}")
        	return []

def get_places_details(place_id):
	base_url = "https://maps.googleapis.com/maps/api/place/details/json"
	params = {
		'place_id': place_id,
		'key': API_KEY
		}

	url = f"{base_url}?{urllib.parse.urlencode(params)}"
	response = requests.get(url)

	try:
		if response.status_code == 200:
			details_data = response.json()
			return details_data.get('result', {})
		else:
			print(f"Error fetching data: {response.status_code}")
			return {}

	except Exception as ex:
		print(f"An error occurred (details): {ex}")
		return {}

def get_photo(photo_reference, max_width = 400):
	base_url = "https://maps.googleapis.com/maps/api/place/photo"
	params = {
		'maxwidth': max_width,
		'photo_reference': photo_reference,
		'key': API_KEY
		}

	url = f"{base_url}?{urllib.parse.urlencode(params)}"

	try:
		response = requests.get(url)
		if response.status_code == 200:
			return url
		else:
			print(f"Error fetching photo. HTTP Status Code: {response.status_code}")
			return 'N/A'

	except requests.exceptions.RequestException as ex:
		print(f"An error occurred: {ex}")
		return 'N/A'