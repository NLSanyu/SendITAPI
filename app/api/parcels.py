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

	query = """SELECT * FROM parcels;"""
	db.connect()
	db.cur.execute(query)
	db.connection.commit()
	result = db.cur.fetchall()
	if result != None:
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': result}), 200
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
	if result != None:
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': result}), 200
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
	
	query = """SELECT * FROM parcels WHERE id = %s AND status != %s;"""
	db.connect()
	db.cur.execute(query, (parcel_id, 'Cancelled',))
	result = db.cur.fetchall()
	if result != None:
		for row in result:
			if row[8] == "Delivered":
				return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
			else:
				query = """UPDATE parcels SET status = %s WHERE id = %s"""
				db.cur.execute(query, ('Cancelled', parcel_id,))
				db.connection.commit()
				db.connection.close()
				return jsonify({'message': 'parcel updated', 'status': 'success'}), 200			
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
	if result != None:
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

	owner = request.json['owner'] 
	pickup_location = request.json['pickup_location'] 
	destination = request.json['destination']  
	description = request.json['description'] 
	if validate_parcel_info(owner, description, pickup_location, destination):
		query = """INSERT INTO parcels (owner, description, date_created, pickup_location, present_location, destination, price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
		db.connect()
		db.cur.execute(query, (owner, description, date_created, pickup_location, present_location, destination, price, status,))
		db.connection.commit()
		return jsonify({'message': 'parcel created', 'status': 'success'}), 201
	else:
		return jsonify({'message': 'parcel not created', 'status': 'failure'}), 400


	

