from datetime import datetime
from login_DB import login_database_blueprint
from optimal_month import optimal_month_blueprint
from addInfoToDB import add_trip_blueprint
from flask import Flask, request, jsonify, render_template, Blueprint
from past_history_database import past_history_database
from HotelFlightRun import hotel_flight_run
import places_API
import recommend_places


app = Flask(__name__)
app.register_blueprint(login_database_blueprint)
app.register_blueprint(add_trip_blueprint)
app.register_blueprint(optimal_month_blueprint)
app.register_blueprint(past_history_database)
app.register_blueprint(hotel_flight_run)
@app.route('/')
def index():
    return render_template('login_page.html') 

@app.route('/pastTrips')
def name4():
    return render_template('pastTrips.html')

@app.route('/boarding')
def name3():
    return render_template('boarding.html')

@app.route('/activities')
def name6():
    return render_template('activities.html')


@app.route('/main_page')
def method_name():
    return render_template('main_page.html')

@app.route('/searchFlight')
def name2():
    return render_template('searchFlight.html')


@app.route('/get_top_restaurants', methods=['GET'])
def get_top_restaurants():
    # Call the recommend_places function to get top recommended restaurants
	top_restaurants = recommend_places.recommend_places(location="33.9720577784,-117.325408698", radius=16000, place_type="restaurant", number_of_recommend=3)
    
    # Return the restaurant data as a JSON response
	return jsonify(top_restaurants)

@app.route('/get_top_bars', methods=['GET'])
def get_top_hotels():
	top_bars = recommend_places.recommend_places(location="33.9720577784,-117.325408698", radius=16000, place_type="bar", number_of_recommend=3)
    
	return jsonify(top_bars)

@app.route('/get_top_attractions', methods=['GET'])
def get_top_attractions():
	top_attractions = recommend_places.recommend_places(location="33.9720577784,-117.325408698", radius=32000, place_type="tourist_attraction", number_of_recommend=3)
    
	return jsonify(top_attractions)

if __name__ == '__main__':
    app.run(debug=True)