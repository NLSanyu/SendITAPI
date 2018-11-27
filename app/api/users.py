import psycopg2
import flasgger
import datetime
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.helpers.user_helpers import validate_user_info, validate_email
from app.api.helpers.parcel_helpers import convert_to_dict
from app.api.helpers.validate_keys import validate_key
from app import app

db = DatabaseConnection()

#api
@app.route('/api/v1', methods=['GET'])
def api_home():
	"""
		Function for API home
	"""
	return "<p>SendIT API</p>"

@app.route('/api/v1/users', methods=['GET'])
@jwt_required
@flasgger.swag_from("./docs/get_all_users.yml")
def get_all_users():
	"""
		Function for API endpoint to fetch all users
	"""
	current_user = get_jwt_identity()
	query = """SELECT * FROM users;"""
	db.connect()
	db.cur.execute(query)
	db.connection.commit()
	result = db.cur.fetchall()
	if result != None:
		db.connection.close()
		return jsonify({'message': 'users retrieved', 'status': 'success', 'data': result}), 200
	else:
		return jsonify({'message':'no users signed up yet', 'status':'failure'}), 200
	
			
	
@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
@jwt_required
@flasgger.swag_from("./docs/get_user_parcels.yml")
def get_user_parcels(user_id):
	"""
		Function for API endpoint to fetch all parcel delivery orders by a specific user
	"""
	current_user = get_jwt_identity()

	query = """SELECT * FROM parcels WHERE owner_id = %s;"""
	db.connect()
	db.cur.execute(query, (user_id,))
	db.connection.commit()
	result = db.cur.fetchall()
	if result:
		parcels = convert_to_dict(result)
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': parcels}), 200
	else:
		return jsonify({'message':'no parcels for this user', 'status':'failure'}), 400
	

@app.route('/api/v1/auth/login', methods=['POST'])
@flasgger.swag_from("./docs/login.yml")
def login_user():
	"""
		Function for API endpoint to log a user in
	"""
	req = request.json
	req_keys = req.keys()
	if not validate_key(req_keys, 'username') and validate_key(req_keys, 'password'):
		return jsonify({'message': 'incomplete data entered: key/keys missing', 'status': 'failure'}), 400
	else:
		username = request.json['username'] 
		password = request.json['password'] 

	if not(validate_user_info(username) and validate_user_info(password)):
		return jsonify({'message': 'invalid data', 'status': 'failure'}), 400
	else:
		#password = generate_password_hash(password)
		query = """SELECT * FROM users WHERE username = %s;"""
		db.connect()
		db.cur.execute(query, (username,))
		db.connection.commit()
		result = db.cur.fetchall()
		if result:
			for row in result:
				req['id'] = row[0]
			access_token = create_access_token(identity = req)
			db.cur.close()
			db.connection.close()
			return jsonify({'message': 'user logged in succesfully', 'status': 'success', 'access_token': access_token}), 200
		else:
			return jsonify({'message': 'user log in failed, user not registered', 'status': 'failure'}), 401

		
	
@app.route('/api/v1/auth/signup', methods=['POST'])
@flasgger.swag_from("./docs/signup.yml")
def create_user():
	"""
		Function for API endpoint to sign a user up
	"""
	req = request.json
	req_keys = req.keys()
	if not(validate_key(req_keys, 'username') and validate_key(req_keys, 'email') and validate_key(req_keys, 'password')):
		return jsonify({'message': 'incomplete data entered: key/keys missing', 'status': 'failure'}), 400
	else:
		username = request.json['username'] 
		email = request.json['email']
		password = request.json['password'] 

	if not(validate_user_info(username) and validate_user_info(email) and validate_email(email) and validate_user_info(password)):
		return jsonify({'message': "user not created because of invalid information", 'status': 'failure'}), 400
	else:
		query = """SELECT * FROM users WHERE username = %s AND email = %s;"""
		db.connect()
		db.cur.execute(query, (username, email,))
		db.connection.commit()
		result = db.cur.fetchall()
		if result:
			return jsonify({'message': "user already exists", 'status': 'failure'}), 400
		else:
			query = """INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"""
			db.cur.execute(query, (username, email, password,))
			db.connection.commit()
			db.cur.close()
			db.connection.close()
			return jsonify({'message': 'user signed up successfully', 'status': 'success'}), 201
		


