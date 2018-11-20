import psycopg2
import datetime
from flask import Flask, request, jsonify, make_response
from app.models.models import DatabaseConnection
from app import app

query = ""
status = "Cancelled"

db = None

@app.route('/api/v1/parcels', methods=['GET'])
def get_all_parcels():
	"""
		Function for API endpoint to fetch all parcel delivery orders
	"""
	query = """SELECT * FROM parcels;"""
	connect_to_db()
	db.cur.execute(query)
	db.connection.commit()
	result = db.cur.fetchall()
	if result != None:
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': result}), 200
	else:
		return jsonify({'message':'no parcels', 'status':'failure'}), 400
	

@app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
def get_parcel(parcel_id):
	"""
		Function for API endpoint to fetch a specific parcel delivery order
	"""
	query = """SELECT * FROM parcels WHERE id = %s;"""
	if type(parcel_id) != int:
		return jsonify({'message': 'id should be an integer', 'status': 'failure'}), 400
	
	connect_to_db()
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
def cancel_order(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	query = """SELECT * FROM parcels WHERE id = %s AND status != %s;"""
	connect_to_db()
	db.cur.execute(query, (parcel_id, status,))
	result = db.cur.fetchall()
	if result != None:
		for row in result:
			if row[8] == "Delivered":
				return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
			else:
				query = """UPDATE parcels SET status = %s WHERE id = %s"""
				db.cur.execute(query, (status, parcel_id,))
				db.connection.commit()
				db.connection.close()
				return jsonify({'message': 'parcel updated', 'status': 'success'}), 200			
		else: 
			db.connection.close()
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 404
		

@app.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'])
def change_parcel_destination(parcel_id):
	"""
		Function for API endpoint to change the destination of a parcel delivery order
	"""
	req = request.json
	if 'destination' not in req.keys():
		return jsonify({'message': 'destination not provided', 'status': 'failure'}), 400

	dest = request.json['destination']
	if dest == "": 
		return jsonify({'message': 'destination is empty', 'status': 'failure'}), 400
	else:
		if len(dest) > 124:
			return jsonify({'message': 'destination should not be longer than 124 characters', 'status': 'failure'}), 400

	query = """SELECT * FROM parcels WHERE id = %s;"""
	connect_to_db()
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
def create_order():
	"""
		Function for API endpoint to create a parcel delivery order
	"""
	
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
		connect_to_db()
		db.cur.execute(query, (owner, description, date_created, pickup_location, present_location, destination, price, status,))
		db.connection.commit()
		return jsonify({'message': 'parcel created', 'status': 'success'}), 200
	else:
		return jsonify({'message': 'parcel not created', 'status': 'failure'}), 400

		#token here

def connect_to_db():
	global db
	db = DatabaseConnection()
	"""
	global conn
	global cur
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
	except (Exception, psycopg2.DatabaseError) as error:
		conn.close()
		return jsonify({'message':'error', 'status':'failure'})
	"""
		


def validate_parcel_info(owner, description, pickup_location, destination):
	"""
		Function to validate parcel info. Making sure the required fields are filled in and correct
	"""

	if type(owner) != int: 
		return jsonify({'message': 'parcel owner must be identified by id (integer)', 'status': 'failure'}), 400

	if description == "": 
		return jsonify({'message': 'description is empty', 'status': 'failure'}), 400
	else:
		if len(description) > 124:
			return jsonify({'message': 'description should not be longer than 124 characters', 'status': 'failure'}), 400

	if pickup_location == "": 
		return jsonify({'message': 'pickup_location is empty', 'status': 'failure'}), 400
	else:
		if len(pickup_location) > 124:
			return jsonify({'message': 'pickup location should not be longer than 124 characters', 'status': 'failure'}), 400

	if destination == "": 
		return jsonify({'message': 'destination is empty', 'status': 'failure'}), 400
	else:
		if len(destination) > 124:
			return jsonify({'message': 'destination should not be longer than 124 characters', 'status': 'failure'}), 400	

	return True
