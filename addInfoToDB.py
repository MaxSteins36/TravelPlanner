from flask import Blueprint, request, jsonify
from user import User
from database import dispatcher
from datetime import datetime

add_trip_blueprint = Blueprint('add_trip', __name__)

@add_trip_blueprint.route('/add_hotel', methods=['POST'])
def add_hotel():
    try:
        data = request.json
        if not data or 'name' not in data:
            return jsonify({"error": "Invalid data, 'name' key is missing"}), 400

        current_user = User.get_current_user()

        hotel_name = data['name']
        room_type = data['room_type']
        bed_type = data['bed_type']
        number_of_beds = int(data['number_of_beds'])
        price = float(data['price'])

        user_id = int(current_user.id)

        query = """
        INSERT INTO Hotels (user_id, name, room_type, bed_type, number_of_beds, price)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        params = (user_id, hotel_name, room_type, bed_type, number_of_beds, price)

        dispatcher.execute(query, params)
        dispatcher.connection.commit()

        return jsonify({"message": "Hotel added successfully!"}), 200

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500


@add_trip_blueprint.route('/add_trip', methods=['POST'])
def add_trip():
    try:
        data = request.json
        if not data or 'flights' not in data:
            return jsonify({"error": "Invalid data, 'flights' key is missing"}), 400

        current_user = User.get_current_user()

        for flight in data['flights']:
            price = float(flight['outbound'][0]['price'])
            currency = flight['outbound'][0]['currency']
            number_of_seats = int(flight['outbound'][0]['number_of_seats'])

            user_id = int(current_user.id)

            query = """
            INSERT INTO Flights (user_id, price, currency, number_of_seats)
            VALUES (?, ?, ?, ?);
            """
            params = (user_id, price, currency, number_of_seats)

            dispatcher.execute(query, params)
            dispatcher.connection.commit()

            flight_id_query = "SELECT last_insert_rowid();"
            result = dispatcher.execute(flight_id_query)

            flight_id = result[0]['last_insert_rowid()'] if isinstance(result, list) else result['last_insert_rowid()']

            for outboundFlight in flight['outbound']:
                if not all(key in outboundFlight for key in ['departure', 'arrival', 'departure_time', 'arrival_time']):
                    print(f"Missing keys in outbound flight: {outboundFlight}")
                    continue

                departure_time = str(outboundFlight['departure_time'])
                arrival_time = str(outboundFlight['arrival_time'])

                segment_query = """
                INSERT INTO Segments (flight_id, type, departure, arrival, departure_time, arrival_time)
                VALUES (?, ?, ?, ?, ?, ?);
                """
                segment_params = (
                    int(flight_id),  # Ensure flight_id is an integer
                    'outbound',  # Segment type
                    outboundFlight['departure'],
                    outboundFlight['arrival'],
                    departure_time,
                    arrival_time
                )

                try:
                    dispatcher.execute(segment_query, segment_params)
                    dispatcher.connection.commit()  # Commit each segment insertion
                except Exception as e:
                    print(f"Error executing segment query: {e}")
                    continue
            
            for inboundFlight in flight['return']:
                if not all(key in inboundFlight for key in ['departure', 'arrival', 'departure_time', 'arrival_time']):
                    print(f"Missing keys in outbound flight: {inboundFlight}")
                    continue

                departure_time = str(outboundFlight['departure_time'])
                arrival_time = str(outboundFlight['arrival_time'])

                segment_query = """
                INSERT INTO Segments (flight_id, type, departure, arrival, departure_time, arrival_time)
                VALUES (?, ?, ?, ?, ?, ?);
                """
                segment_params = (
                    int(flight_id), 
                    'return',
                    inboundFlight['departure'],
                    inboundFlight['arrival'],
                    departure_time,
                    arrival_time
                )

                try:
                    dispatcher.execute(segment_query, segment_params)
                    dispatcher.connection.commit() 
                except Exception as e:
                    print(f"Error executing segment query: {e}")
                    continue
        return jsonify({"message": "Trips and segments added successfully!"}), 200

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

