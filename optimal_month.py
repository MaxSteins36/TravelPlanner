from datetime import date, timedelta, datetime
import calendar
import dotenv
import os
import asyncio
import aiohttp
from itertools import islice
from flask import Blueprint, request, jsonify
from base import AmadeusBase

optimal_month_blueprint = Blueprint('optimal_month', __name__)

dotenv.load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

month_bank = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}
cabin_data = {
    'ECONOMY': [],
    'PREMIUM_ECONOMY': [],
    'BUSINESS': [],
    'FIRST_CLASS': []
}

def chunk_tasks(tasks, chunk_size):
    it = iter(tasks)
    for first in it:
        yield [first] + list(islice(it, chunk_size- 1))
async def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': API_SECRET,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as r:
                if r.status == 200:
                    access_token = await r.json()
                    print("Access Token:", access_token.get('access_token'))
                    return access_token.get('access_token')
                else:
                    print("Failed to retrieve token:", r.status, await r.text())
    except Exception as e:
        print('Program failed:', e)

def valid_day_for_month(year, month, day):
    _, num_days_in_month = calendar.monthrange(year, month)
    return 1 <= day <= num_days_in_month

async def get_flight_API(session, access_token, parameters):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {access_token}'}
    csv_path = "flight_data.txt"

    async with session.get(url, headers=headers, params=parameters) as response:
        if response.status == 200:
            flight_data = await response.json()
            flights = []


            for flight in flight_data.get("data", []):
                flight_id = flight.get("id")
                itineraries = flight.get("itineraries", [])
                traveler_class = flight.get("travelerPricings", [])
                price = flight.get("price", {}).get("grandTotal", "N/A")
                currency = flight.get("price", {}).get("currency", "N/A")
                airline_code = flight.get("validatingAirlineCodes", [])[0]

                outbound = {}
                inbound = {}
                for index, itinerary in enumerate(itineraries):
                    segments = itinerary.get("segments", [])

                    if index == 0:
                        for segment in segments:
                            departure = segment.get("departure", {})
                            arrival = segment.get("arrival", {})
                            carrier_code = segment.get("number")

                            if 'at' in departure:
                                outbound = {
                                    'departure_time': departure.get('at'),
                                    'price': price,
                                    'currency': currency,
                                    'airline': airline_code,
                                    'return_date': arrival.get('at'),
                                    'segmentId': None,
                                    'cabin': None,
                                    'carrier_code': carrier_code,
                                    'id': f'#{flight_id}',
                                }

                    elif index == 1:
                        for segment in segments:
                            departure = segment.get("departure", {})
                            arrival = segment.get("arrival", {})
                            carrier_code = segment.get("number")

                            if 'at' in departure:
                                inbound = {
                                    'departure_time': departure.get('at'),
                                    'price': price,
                                    'currency': currency,
                                    'airline': airline_code,
                                    'return_date': arrival.get('at'),
                                    'segmentId': None,
                                    'cabin': None,
                                    'carrier_code': carrier_code,
                                    'id': f'#{flight_id}',
                                }

                for traveler in traveler_class:
                    for segment in traveler.get("fareDetailsBySegment", []):
                        segmentId = segment.get("segmentId")
                        cabin = segment.get("cabin")

                        if outbound.get('segmentId') is None:
                            outbound['segmentId'] = segmentId
                            outbound['cabin'] = cabin
                        elif inbound.get('segmentId') is None:
                            inbound['segmentId'] = segmentId
                            inbound['cabin'] = cabin

                combined_data = {
                    'outbound': outbound,
                    'inbound': inbound
                }

                filtered_flight_data = filter_by_cabin(combined_data)
                flights.extend(filtered_flight_data)

            return flights
        else:
            print(f"Failed to retrieve flights:", response.status, await response.text())
            return []
def filter_by_cabin(combined_data):
    global cabin_data

    print("Processing combined_data:", combined_data)

    outbound = combined_data.get('outbound')
    inbound = combined_data.get('inbound')

    filtered_flights = []

    if outbound:
        price = outbound.get('price')
        currency = outbound.get('currency')
        cabin = outbound.get('cabin')

        if price is not None and currency is not None:
            try:
                price_float = float(price)
                flight_details = {
                    'departure_time': outbound.get('departure_time'),
                    'price': price_float,
                    'currency': currency,
                    'airline': outbound.get('airline'),
                    'return_date': inbound.get('return_date') if inbound else None,
                    'segmentId': outbound.get('segmentId'),
                    'cabin': cabin,
                    'id': outbound.get('id'),
                    'outbound': outbound,
                    'inbound': inbound
                }


                if cabin in cabin_data:
                    cabin_data[cabin].append(flight_details)


                filtered_flights.append(flight_details)

            except ValueError:

                print(f"Invalid price encountered: {price} in outbound data:", outbound)

    return filtered_flights


async def split_month_call_api(access_token, origin, destination, month, dif_day, adults):
    current_day = date.today()
    current_month = current_day.month
    selected_month = int(month_bank[month])

    year = current_day.year + 1 if current_month >= selected_month else current_day.year

    _, days_in_month = calendar.monthrange(year, selected_month)
    
    start_date = date(year=year, month=selected_month, day=1)

    end_day = dif_day + 1
    
    if not valid_day_for_month(year, selected_month, end_day):
        raise ValueError(f"The day {end_day} is out of range for month {selected_month}.")
    end_date = date(year=year, month=selected_month, day=dif_day+1)
    


    ranges = []
    for day in range(days_in_month):
        start = start_date + timedelta(days=day)
        end = end_date + timedelta(days=day)

        ranges.append((start, end))



    async with aiohttp.ClientSession() as session:
        tasks = []
        for start, end in ranges:
            formatted_start_date = start.strftime('%Y-%m-%d')
            formatted_end_date = end.strftime('%Y-%m-%d')
            parameters = {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": formatted_start_date,
                "returnDate": formatted_end_date,
                "adults": adults
            }
            task = asyncio.create_task(get_flight_API(session, access_token, parameters))
            tasks.append(task)

        chunk_size =4
        all_flights = []
        for chunk in chunk_tasks(tasks, chunk_size):
            chunk_flights = await asyncio.gather(*chunk)
            for flights in chunk_flights:
                all_flights.extend(flights)

            economy_data_sorted = sorted([flight for flight in all_flights if flight['cabin'] == 'ECONOMY'],
                                         key=lambda x: float(x['price']))
            top_5_economy = economy_data_sorted[:5]

            premium_economy_data_sorted = sorted(
                [flight for flight in all_flights if flight['cabin'] == 'PREMIUM_ECONOMY'],
                key=lambda x: float(x['price']))
            top_5_premium_economy = premium_economy_data_sorted[:5]
            print(f"TOP 5 {top_5_economy}")
            business_data_sorted = sorted([flight for flight in all_flights if flight['cabin'] == 'BUSINESS'],
                                          key=lambda x: float(x['price']))
            top_5_business = business_data_sorted[:5]

            first_class_data_sorted = sorted([flight for flight in all_flights if flight['cabin'] == 'FIRST_CLASS'],
                                             key=lambda x: float(x['price']))
            top_5_first_class = first_class_data_sorted[:5]

            return top_5_economy, top_5_premium_economy, top_5_business, top_5_first_class


@optimal_month_blueprint.route('/get_optimal_month', methods=['POST'])
async def get_optimal_month():
    AmadeusBase
    data = request.get_json()
    print("im here")
    origin = data['origin']
    destination = data['destination']
    month = data['month']
    departureDate = data['departureDate']
    print(departureDate)
    returnDate = data['returnDate']
    adults = data['adults']
    departureDate = datetime.strptime(departureDate, "%Y-%m-%d")  
    returnDate = datetime.strptime(returnDate, "%Y-%m-%d")  

    dif_day = (returnDate - departureDate).days  
    amadeues_instance = AmadeusBase()
    origin = amadeues_instance.get_iata_code(origin)
    destination = amadeues_instance.get_iata_code(destination)
    access_token = await get_access_token()
    if access_token:
        results = await split_month_call_api(access_token, origin, destination, month, dif_day, adults)
        #([{'departure_time': '2025-04-03T08:30:00', 'price': 638.62, 'currency': 'EUR', 'airline': 'MF', 'return_date': '2025-04-08T19:40:00', 'segmentId': '65', 'cabin': 'ECONOMY', 'id': '#1', 'outbound': {'departure_time': '2025-04-03T08:30:00', 'price': '638.62', 'currency': 'EUR', 'airline': 'MF', 'return_date': '2025-04-03T13:45:00', 'segmentId': '65', 'cabin': 'ECONOMY', 'carrier_code': '815', 'id': '#1'}, 'inbound': {'departure_time': '2025-04-08T22:10:00', 'price': '638.62', 'currency': 'EUR', 'airline': 'MF', 'return_date': '2025-04-08T19:40:00', 'segmentId': '66', 'cabin': 'ECONOMY', 'carrier_code': '829', 'id': '#1'}}, {'departure_time': '2025-04-02T08:15:00', 'price': 855.98, 'currency': 'EUR', 'airline': 'CX', 'return_date': '2025-04-08T22:15:00', 'segmentId': '25', 'cabin': 'ECONOMY', 'id': '#2', 'outbound': {'departure_time': '2025-04-02T08:15:00', 'price': '855.98', 'currency': 'EUR', 'airline': 'CX', 'return_date': '2025-04-02T13:40:00', 'segmentId': '25', 'cabin': 'ECONOMY', 'carrier_code': '526', 'id': '#2'}, 'inbound': {'departure_time': '2025-04-09T00:05:00', 'price': '855.98', 'currency': 'EUR', 'airline': 'CX', 'return_date': '2025-04-08T22:15:00', 'segmentId': '26', 'cabin': 'ECONOMY', 'carrier_code': '880', 'id': '#2'}}, {'departure_time': '2025-04-02T09:05:00', 'price': 855.98, 'currency': 'EUR', 'airline': 'CX', 'return_date': '2025-04-08T22:15:00', 'segmentId': '15', 'cabin': 'ECONOMY', 'id': '#3', 'outbound': {'departure_time': '2025-04-02T09:05:00', 'price': '855.98', 'currency': 'EUR', 'airline': 'CX', 'return_date': '2025-04-02T14:30:00', 'segmentId': '15', 'cabin': 'ECONOMY', 'carrier_code': '504', 'id': '#3'}, 'inbound': {'departure_time': '2025-04-09T00:05:00', 'price': '855.98', 'currency': 'EUR', 'airline': 'CX', 'return_date': '2025-04-08T22:15:00', 'segmentId': '16', 'cabin': 'ECONOMY', 'carrier_code': '880', 'id': '#3'}}, {'departure_time': '2025-04-03T08:30:00', 'price': 915.25, 'currency': 'EUR', 'airline': 'MF', 'return_date': '2025-04-08T21:55:00', 'segmentId': '65', 'cabin': 'ECONOMY', 'id': '#4', 'outbound': {'departure_time': '2025-04-03T08:30:00', 'price': '915.25', 'currency': 'EUR', 'airline': 'MF', 'return_date': '2025-04-03T13:45:00', 'segmentId': '65', 'cabin': 'ECONOMY', 'carrier_code': '815', 'id': '#4'}, 'inbound': {'departure_time': '2025-04-08T13:20:00', 'price': '915.25', 'currency': 'EUR', 'airline': 'MF', 'return_date': '2025-04-08T21:55:00', 'segmentId': '66', 'cabin': 'ECONOMY', 'carrier_code': '80', 'id': '#4'}}, {'departure_time': '2025-04-03T09:00:00', 'price': 969.72, 'currency': 'EUR', 'airline': 'OZ', 'return_date': '2025-04-08T16:00:00', 'segmentId': '37', 'cabin': 'ECONOMY', 'id': '#5', 'outbound': {'departure_time': '2025-04-03T09:00:00', 'price': '969.72', 'currency': 'EUR', 'airline': 'OZ', 'return_date': '2025-04-03T11:20:00', 'segmentId': '37', 'cabin': 'ECONOMY', 'carrier_code': '102', 'id': '#5'}, 'inbound': {'departure_time': '2025-04-08T20:40:00', 'price': '969.72', 'currency': 'EUR', 'airline': 'OZ', 'return_date': '2025-04-08T16:00:00', 'segmentId': '38', 'cabin': 'ECONOMY', 'carrier_code': '204', 'id': '#5'}}], [], [], [])
        return jsonify({
            "optimal_month_results": results if results else []
        }), 200