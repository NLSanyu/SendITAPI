import psycopg2
import datetime
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from app.api.helpers.validate_parcels import validate_parcel_info
from app import app

db = DatabaseConnection()

@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def get_all_parcels():
	"""
		Function for API endpoint to fetch all parcel delivery orders
	"""
	current_user = get_jwt_identity()

	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400

	query = """SELECT * FROM parcels;"""
	db.connect()
	db.cur.execute(query)
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
		return jsonify({'message':'no parcels', 'status':'failure'}), 400
	

@app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
@jwt_required
def get_parcel(parcel_id):
	"""
		Function for API endpoint to fetch a specific parcel delivery order
	"""
	current_user = get_jwt_identity()

	query = """SELECT * FROM parcels WHERE id = %s;"""
	
	db.connect()
	db.cur.execute(query, (parcel_id,))
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
		if current_user['id'] != data['owner_id']:
			return jsonify({'message': 'access denied', 'status': 'failure'}), 400
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': data_list}), 200
	else:
		db.connection.close()
		return jsonify({'message': 'no parcel with this id', 'status': 'failure'}), 400


@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
@jwt_required
def cancel_order(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	current_user = get_jwt_identity()
	
	query = """SELECT * FROM parcels WHERE id = %s;"""
	db.connect()
	db.cur.execute(query, (parcel_id,))
	result = db.cur.fetchall()
	if result:
		for row in result:
			id = row[1]
			name = get_owner_name(id)
			if current_user['username'] != name:
				return jsonify({'message': 'access denied', 'status': 'failure'}), 400
			if row[8] == "Delivered":
				return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
			else:
				query = """UPDATE parcels SET status = %s WHERE id = %s"""
				status = "Cancelled"
				db.cur.execute(query, (status, parcel_id,))
				db.connection.commit()
				db.connection.close()
				return jsonify({'message': 'parcel cancelled', 'status': 'success'}), 200			
		else: 
			db.connection.close()
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400
		

@app.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'])
@jwt_required
def change_parcel_destination(parcel_id):
	"""
		Function for API endpoint to change the destination of a parcel delivery order
	"""
	current_user = get_jwt_identity()

	req = request.json
	if 'destination' in req.keys():
		dest = request.json['destination']
		if dest == "": 
			return jsonify({'message': 'destination is empty', 'status': 'failure'}), 400
		else:
			if len(dest) > 124:
				return jsonify({'message': 'destination should not be longer than 124 characters', 'status': 'failure'}), 400

	query = """SELECT * FROM parcels WHERE id = %s;"""
	db.connect()
	db.cur.execute(query, (parcel_id,))
	db.connection.commit()
	result = db.cur.fetchall()
	if result:
		for row in result:
			if (row[8] == "Delivered" or row[8] == "Cancelled"):
				return jsonify({'message': 'parcel already delivered or cancelled', 'status': 'failure'}), 400
			else:
				query = """UPDATE parcels SET destination = %s WHERE id = %s"""
				db.cur.execute(query, (dest, parcel_id,))	
				db.connection.commit()
				return jsonify({'message': 'parcel destination changed', 'status': 'success'}), 400
	else: 
		return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 404

	db.connection.close()

@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
def create_parcel_order():
	"""
		Function for API endpoint to create a parcel delivery order
	"""
	current_user = get_jwt_identity()
	
	date = datetime.datetime.now()
	date_string = str(date.day) + "-" + str(date.month) + "-" + str(date.year)

	date_created = date_string
	present_location = request.json['pickup_location']
	price = ' '
	status = 'New'

	owner = request.json['owner_id'] 
	pickup_location = request.json['pickup_location'] 
	destination = request.json['destination']  
	description = request.json['description'] 
	if validate_parcel_info(owner, description, pickup_location, destination):
		query = """INSERT INTO parcels (owner_id, description, date_created, pickup_location, present_location, destination, price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
		db.connect()
		db.cur.execute(query, (owner, description, date_created, pickup_location, present_location, destination, price, status,))
		db.connection.commit()
		return jsonify({'message': 'parcel created', 'status': 'success'}), 201
	else:
		return jsonify({'message': 'parcel not created', 'status': 'failure'}), 400


def get_owner_name(owner_id):
	query = """SELECT * FROM users WHERE id = %s"""
	db.cur.execute(query, (owner_id,))
	result = db.cur.fetchall()
	for row in result:
		name = row[1]
	return name
