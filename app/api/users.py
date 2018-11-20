import psycopg2
import datetime, re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from flask import Flask, request, jsonify, make_response
from app import app

db = None

#api
@app.route('/api/v1', methods=['GET'])
def api_home():
	"""
		Function for API home
	"""
	return "<p>SendIT API</p>"

@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def get_all_users():
	"""
		Function for API endpoint to fetch all users
	"""
	current_user = get_jwt_identity()
	query = """SELECT * FROM users;"""
	connect_to_db()
	db.cur.execute(query)
	db.connection.commit()
	result = db.cur.fetchall()
	if result != None:
		db.connection.close()
		return jsonify({'message': 'users retrieved', 'status': 'success', 'data': result}), 200
	else:
		return jsonify({'message':'no users', 'status':'failure'}), 400
	
			
	
@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
@jwt_required
def get_user_parcel(user_id):
	"""
		Function for API endpoint to fetch all parcel delivery orders by a specific user
	"""
	current_user = get_jwt_identity()
	if type(user_id) != int:
		return jsonify({'message':'user must be identified by an integer', 'status':'failure'}), 400

	query = """SELECT * FROM parcels WHERE owner = %s;"""
	connect_to_db()
	db.cur.execute(query, (user_id,))
	db.connection.commit()
	result = db.cur.fetchall()
	if result != None:
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': result}), 200
	else:
		return jsonify({'message':'no parcels for this user', 'status':'failure'}), 400
	

@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
	"""
		Function for API endpoint to log a user in
	"""
	req = request.json
	if 'username' in req.keys():
		username = request.json['username'] 
	if 'password' in req.keys():
		password = request.json['password'] 
	email=""

	if validate_user_info(username, email, password, False):
		password = generate_password_hash(password)
		query = """SELECT * FROM users WHERE username = %s AND password_hash = %s;"""
		connect_to_db()
		db.cur.execute(query, (username, password,))
		db.connection.commit()
		result = db.cur.fetchall()
		if result != None:
			db.cur.close()
			db.connection.close()
			access_token = create_access_token(identity = username)
			return jsonify({'message': 'user logged in', 'status': 'success', 'access_token': access_token}), 200
		else:
			return jsonify({'message': 'user log in failed', 'status': 'failure'})


@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
	"""
		Function for API endpoint to sign a user up
	"""
	req = request.json
	if 'username' in req.keys():
		username = request.json['username'] 
	if 'email' in req.keys():
		email = request.json['email'] 
	if 'password' in req.keys(): 
		password = request.json['password'] 

	#password_hash = generate_password_hash(password)

	if validate_user_info(username, email, password, True):
		query = """INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"""
		connect_to_db()
		db.cur.execute(query, (username, email, password,))
		db.connection.commit()
		db.cur.close()
		db.connection.close()
		return jsonify({'message': "user created"}), 201
	else:
		return jsonify({'message': "user not created", 'status': 'failure'}), 400


def validate_user_info(username, email, password, signup):
	"""
		Function to validate user inputs. Making sure the required fields are filled in and correct
	"""

	if username == "": 
		return jsonify({'message': 'username is empty', 'status': 'failure'}), 400
	else:
		if len(username) > 32:
			return jsonify({'message': 'username should not longer than 32 characters', 'status': 'failure'}), 400	

	if password == "": 
		return jsonify({'message': 'password is empty', 'status': 'failure'}), 400
	else:
		if len(password) < 6:
			return jsonify({'message': 'password should be longer than 6 characters', 'status': 'failure'}), 400	

	if signup:
		if email == "": 
			return jsonify({'message': 'email address is empty', 'status': 'failure'}), 400
		else:
			pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
			if not re.match(pattern, email):
				return jsonify({'message': 'enter a valid email', 'status': 'failure'}), 400

	return True


def connect_to_db():
	global db
	db = DatabaseConnection()