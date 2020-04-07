import psycopg2
import flasgger
import datetime
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.helpers.user_helpers import validate_email
from app.api.helpers.parcel_helpers import convert_to_dict
from app.api.helpers.user_helpers import convert_users_to_dict, convert_one_user_to_dict
from app.api.helpers.validate_info import validate_key, validate
from app import app

db = DatabaseConnection()

@app.route('/api/v1', methods=['GET'])
def api_home():
	"""
		Function for API home
	"""
	return "<p>SendIT API</p>"
	
@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
@jwt_required
@flasgger.swag_from("./docs/get_user_parcels.yml")
def get_user_parcels(user_id):
	"""
		Function for API endpoint to fetch all parcel delivery orders by a specific user
	"""
	current_user = get_jwt_identity()

	query = """SELECT * FROM parcels WHERE owner_id = %s ORDER BY id DESC;"""
	db.cur.execute(query, (user_id,))
	result = db.cur.fetchall()
	if result:
		parcels = convert_to_dict(result)
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

	if not(validate(username) and validate(password)):
		return jsonify({'message': 'invalid data', 'status': 'failure'}), 400
	else:
		query = """SELECT * FROM users WHERE username = %s AND password_hash = %s;"""
		db.cur.execute(query, (username, password,))
		result = db.cur.fetchone()
		if result:
			req['id'] = result[0]
			expiry = datetime.timedelta(days=1)
			access_token = create_access_token(identity = req, expires_delta=expiry)
			user_info = convert_one_user_to_dict(result)
			return jsonify({'message': 'user logged in succesfully', 'status': 'success', 'access_token': access_token, 'user_info': user_info}), 200
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
		if validate_key(req_keys, 'phone_number'):
			phone_number = request.json['phone_number']
		else:
			phone_number = "none"

		if validate_key(req_keys, 'full_name'):
			full_name = request.json['full_name']
		else:
			full_name = "none"

	if not(validate(username) and validate(email) and validate_email(email) and validate(password)):
		return jsonify({'message': "user not created because of invalid username, email or password", 'status': 'failure'}), 400
	else:
		query = """SELECT * FROM users WHERE username = %s AND email = %s;"""
		db.cur.execute(query, (username, email,))
		result = db.cur.fetchall()
		if result:
			return jsonify({'message': "user already exists", 'status': 'failure'}), 400
		else:
			query = """INSERT INTO users (full_name, username, email, phone_number, password_hash) VALUES (%s, %s, %s, %s, %s)"""
			db.cur.execute(query, (full_name, username, email, phone_number, password))
			return jsonify({'message': 'user signed up successfully', 'status': 'success'}), 201
		


