import psycopg2
import datetime
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.helpers.validate_users import validate_user_info
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
		data_list = []
		data = dict()
		for row in result:
			data['parcel_id'] = row[0]
			data['owner_id'] = row[1]
			data['description'] = row[2]
			data['date_created'] = row[3]
			data['pickup_location'] = row[4]
			data['present_location'] = row[5]
			data['destination'] = row[6]
			data['price'] = row[7]
			data['status'] = row[8]
			data_list.append(data)
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': data_list}), 200
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
			return jsonify({'message': 'user log in failed', 'status': 'failure'}), 400
	

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
	else:
		return jsonify({'message': "user not created because of invalid info", 'status': 'failure'}), 400


