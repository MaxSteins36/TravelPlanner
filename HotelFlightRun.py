from Flights import FlightSearch
from Hotels import HotelSearch
from flask import Flask, request, jsonify, render_template, Blueprint

hotel_flight_run = Blueprint('hotel_flight_run', __name__)
@hotel_flight_run.route('/api/search', methods = ['POST'])
def method_name():
    data = request.json
    origin = data['origin']
    destination = data['destination']
    departure_date = data['departureDate']
    return_date = data.get('returnDate')
    adults = int(data['adults'])
    city = data['city']
    check_in_date = data['checkInDate']
    check_out_date = data['checkOutDate']
    room_quantity = int(data['roomQuantity'])

    flight_search = FlightSearch()
    hotel_search = HotelSearch()
    flights_result = flight_search.search_flights(origin, destination, departure_date, adults, return_date)
    #flights_result = [{'price': '146.23', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'LAX', 'arrival': 'DFW', 'departure_time': '2025-01-20T22:30:00', 'arrival_time': '2025-01-21T03:40:00'}], 'return': [{'departure': 'DFW', 'arrival': 'DEN', 'departure_time': '2025-01-25T22:59:00', 'arrival_time': '2025-01-26T00:27:00'}, {'departure': 'DEN', 'arrival': 'LAX', 'departure_time': '2025-01-26T19:06:00', 'arrival_time': '2025-01-26T20:40:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'LAS', 'departure_time': '2025-01-25T09:35:00', 'arrival_time': '2025-01-25T10:36:00'}, {'departure': 'LAS', 'arrival': 'ONT', 'departure_time': '2025-01-25T19:00:00', 'arrival_time': '2025-01-25T20:09:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'LAS', 'departure_time': '2025-01-25T18:00:00', 'arrival_time': '2025-01-25T19:14:00'}, {'departure': 'LAS', 'arrival': 'ONT', 'departure_time': '2025-01-26T08:00:00', 'arrival_time': '2025-01-26T09:06:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'LAS', 'departure_time': '2025-01-25T09:35:00', 'arrival_time': '2025-01-25T10:36:00'}, {'departure': 'LAS', 'arrival': 'ONT', 'departure_time': '2025-01-26T08:00:00', 'arrival_time': '2025-01-26T09:06:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'LAS', 'departure_time': '2025-01-25T18:00:00', 'arrival_time': '2025-01-25T19:14:00'}, {'departure': 'LAS', 'arrival': 'ONT', 'departure_time': '2025-01-26T19:00:00', 'arrival_time': '2025-01-26T20:09:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'DEN', 'departure_time': '2025-01-25T22:59:00', 'arrival_time': '2025-01-26T00:27:00'}, {'departure': 'DEN', 'arrival': 'ONT', 'departure_time': '2025-01-26T10:52:00', 'arrival_time': '2025-01-26T12:15:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'DEN', 'departure_time': '2025-01-25T15:00:00', 'arrival_time': '2025-01-25T16:27:00'}, {'departure': 'DEN', 'arrival': 'ONT', 'departure_time': '2025-01-26T10:52:00', 'arrival_time': '2025-01-26T12:15:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'LAS', 'departure_time': '2025-01-20T08:00:00', 'arrival_time': '2025-01-20T09:21:00'}, {'departure': 'LAS', 'arrival': 'DFW', 'departure_time': '2025-01-20T11:32:00', 'arrival_time': '2025-01-20T16:29:00'}], 'return': [{'departure': 'DFW', 'arrival': 'DEN', 'departure_time': '2025-01-25T22:59:00', 'arrival_time': '2025-01-26T00:27:00'}, {'departure': 'DEN', 'arrival': 'ONT', 'departure_time': '2025-01-26T22:20:00', 'arrival_time': '2025-01-26T23:39:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'DEN', 'departure_time': '2025-01-20T00:49:00', 'arrival_time': '2025-01-20T04:10:00'}, {'departure': 'DEN', 'arrival': 'DFW', 'departure_time': '2025-01-20T09:42:00', 'arrival_time': '2025-01-20T12:50:00'}], 'return': [{'departure': 'DFW', 'arrival': 'LAS', 'departure_time': '2025-01-25T09:35:00', 'arrival_time': '2025-01-25T10:36:00'}, {'departure': 'LAS', 'arrival': 'ONT', 'departure_time': '2025-01-25T19:00:00', 'arrival_time': '2025-01-25T20:09:00'}]}, {'price': '149.86', 'currency': 'EUR', 'number_of_seats': 3, 'outbound': [{'departure': 'ONT', 'arrival': 'DEN', 'departure_time': '2025-01-20T00:49:00', 'arrival_time': '2025-01-20T04:10:00'}, {'departure': 'DEN', 'arrival': 'DFW', 'departure_time': '2025-01-20T09:42:00', 'arrival_time': '2025-01-20T12:50:00'}], 'return': [{'departure': 'DFW', 'arrival': 'LAS', 'departure_time': '2025-01-25T18:00:00', 'arrival_time': '2025-01-25T19:14:00'}, {'departure': 'LAS', 'arrival': 'ONT', 'departure_time': '2025-01-26T08:00:00', 'arrival_time': '2025-01-26T09:06:00'}]}]
    hotels_result = hotel_search.search_hotels(city, check_in_date, check_out_date, adults, room_quantity)
    #hotels_result = [{'name': 'Best Western Plus DFW Airport Suites', 'room_type': 'SUITE', 'bed_type': 'KING', 'price': '940.95', 'number_of_beds': 1}, {'name': 'HOMEWOOD STES IRVING DFW ARPT', 'room_type': 'SUITE', 'bed_type': 'KING', 'price': '920.12', 'number_of_beds': 1}, {'name': 'HOLIDAY INN EXP STES AIRPORT N', 'room_type': 'SUITE', 'bed_type': 'KING', 'price': '605.69', 'number_of_beds': 1}, {'name': 'Sheraton DFW Airport Hotel', 'room_type': 'Not Available', 'bed_type': 'Not Available', 'price': 'Not Available', 'number_of_beds': 'Not specified'}, {'name': 'The Westin Dallas Fort Worth Airport', 'room_type': 'Not Available', 'bed_type': 'Not Available', 'price': 'Not Available', 'number_of_beds': 'Not specified'}, {'name': 'SUPERMEDIA HOTEL', 'room_type': 'Not Available', 'bed_type': 'Not Available', 'price': 'Not Available', 'number_of_beds': 'Not specified'}]
    combined_data = []  # Initialize a list to collect flight data

    for flight in flights_result:  # Iterate over each flight in the results
        price = flight.get("price", "N/A")
        currency = flight.get("currency", "N/A")
        numSeats = flight.get("number_of_seats", "N/A")
        outbound = flight.get('outbound', [])
        return_ = flight.get('return', [])

        outbound_flights = []
        return_flights = []

        for segment in outbound:
            outbound_flights.append({
                'departure': segment.get('departure'),
                'arrival': segment.get('arrival'),
                'departure_time': segment.get('departure_time'),
                'arrival_time': segment.get('arrival_time'),
                'number_of_seats': numSeats,
                'price': price,
                'currency': currency
            })

        for segment in return_:
            return_flights.append({
                'departure': segment.get('departure'),
                'arrival': segment.get('arrival'),
                'departure_time': segment.get('departure_time'),
                'arrival_time': segment.get('arrival_time'),
                'price': price,
                'currency': currency
            })

        combined_data.append({
            'outbound': outbound_flights,
            'return': return_flights
        })

    return jsonify({"flights": combined_data, "hotels": hotels_result})