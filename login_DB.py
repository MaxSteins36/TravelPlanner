from flask import Blueprint, jsonify, request
from user import User
from database import dispatcher

login_database_blueprint = Blueprint('login_database_blueprint', __name__)

def check_user_exists(username, password):
    print("im here")
    query = "SELECT * FROM user_data WHERE username = ? AND password = ?"
    result = dispatcher.execute(query, (username, password))
    if bool(result):
        User.login(username, password)
    return bool(result)

def add_user_to_database(first_name, last_name, username, password, table):
    query = f"INSERT INTO {table} (username, first_name, last_name, password) VALUES (?, ?, ?, ?)"
    data = (username, first_name, last_name, password)
    try:
        dispatcher.execute(query, data)
        return True
    except Exception as e:
        print(f"Insert error: {e}")
        return False

@login_database_blueprint.route('/login_user', methods=['POST'])
def database_access():
    print("Received request at /database")
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username, password)
    if check_user_exists(username, password):
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200

@login_database_blueprint.route('/add_user', methods=['POST'])
def add_user():
    print("Received request at /add_user")
    table = 'user_data'
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    password = data['password']
    if add_user_to_database(first_name, last_name, username, password, table):
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200
