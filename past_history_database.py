from flask import Flask, Blueprint, jsonify
from user import User

past_history_database = Blueprint('past_history_database', __name__)

@past_history_database.route('/past_history', methods=['GET'])
def past_history():
    print("IN PYTHON")
    
    current_user = User.get_current_user()
    if not current_user:
        return jsonify({"error": "No user is currently logged in"}), 401
    
    try:
        # Get past flight and hotel information
        past_flights = current_user.get_flight_information()
        past_hotels = current_user.get_hotel_information()

        # Ensure past_flights and past_hotels are not None, and return empty lists if so
        past_flights = past_flights if past_flights else []
        past_hotels = past_hotels if past_hotels else []

        print("Past Flights: ", past_flights)
        print("Past Hotels: ", past_hotels)

        return jsonify({
            "past_flights": past_flights,
            "past_hotels": past_hotels
        }), 200

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error fetching data: {str(e)}")
        return jsonify({"error": "Error fetching past history data"}), 500
@past_history_database.route('/get_user_credentials', methods=['GET'])
def get_credentials():
    user = User.get_current_user()
    if user:
        first_name_result = user.get_first_name()  # Call the method
        last_name_result = user.get_last_name()    # Call the method

        # Ensure that results are not empty or None
        if first_name_result and len(first_name_result) > 0:
            first_name = first_name_result[0]['first_name']  # Assuming the result is a list of dicts
        else:
            first_name = None
        print(first_name)
        if last_name_result and len(last_name_result) > 0:
            last_name = last_name_result[0]['last_name']  # Same for last_name
        else:
            last_name = None

        # Return the credentials or an error message if no data is found
        if first_name and last_name:
            return jsonify({
                "first_name": first_name,
                "last_name": last_name
            })
        return jsonify({"error": "User credentials not found"}), 404

    return jsonify({"error": "No user is currently logged in"}), 401
