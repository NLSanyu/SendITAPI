import psycopg2
import datetime
from flask import Flask, request, jsonify, abort, make_response
from app import app

conn = None
cur = None
query = ""
status = "Cancelled"

@app.route('/api/v1/parcels', methods=['GET'])
def get_all_parcels():
	"""
		Function for API endpoint to fetch all parcel delivery orders
	"""
	query = """SELECT * FROM parcels;"""
	connect()
	cur.execute(query)
	conn.commit()
	result = cur.fetchall()
	if result != None:
		parcel_dict = dict()
		for row in result:
			parcel_dict['id'] = row[1]
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': parcel_dict}), 200
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
	
	connect()
	cur.execute(query, (parcel_id,))
	result = cur.fetchall()	
	if result != None:
		parcel_dict = dict()
		for row in result:
			parcel_dict['id'] = row[0]
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': parcel_dict}), 200
	else:
		return jsonify({'message': 'no parcel with this id', 'status': 'failure'}), 400


@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
def cancel_order(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	query = """SELECT * FROM parcels WHERE id=%d AND status <> %s;"""
	connect()
	cur.execute()
	result = cur.fetchall()
	if result != None:
		for row in cur:
			if row[9] == "Delivered":
				abort(400, 'Parcel already delivered')
			else:
				query = """UPDATE parcels SET status = %s WHERE id = %s"""
				cur = conn.cursor()
				cur.execute(query, (status, parcel_id, ))	
		else: 
			abort(404, 'Parcel non-existent')	
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
		cur.execute(query, (parcel_id, status,))
		conn.commit()
		if cur.fetchall:
			for row in cur:
				if row[9] == "Delivered":
					abort(400, 'Parcel already delivered')
				else:
					query = """UPDATE parcels SET status = %s WHERE id = %s"""
					cur = conn.cursor()
					cur.execute(query, (status, parcel_id, ))	
		else: 
			abort(404, 'Parcel non-existent')	
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


@app.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'])
def change_parcel_destination(parcel_id):
	"""
		Function for API endpoint to change the destination of a parcel delivery order
	"""
	dest = request.json['destination']
	if dest == "": 
		return jsonify({'Message': 'Destination is empty'}), 400
	else:
		if len(dest) > 124:
			return jsonify({'Message': 'Destination should not be longer than 124 characters'}), 400

	query = """SELECT * FROM parcels WHERE id=%d;"""
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
		cur.execute(query, (parcel_id,))
		conn.commit()
		if cur.fetchall:
			for row in cur:
				if row[9] == "Delivered":
					abort(400, 'Parcel already delivered')
				else:
					query = """UPDATE parcels SET destination = %s WHERE id = %s"""
					cur = conn.cursor()
					cur.execute(query, (dest, parcel_id, ))	
		else: 
			abort(404, 'Parcel non-existent')	
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

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
		query = """ INSERT INTO parcels VALUES (%d, %s, %s, %s, %s, %s, %s, %s)"""
		conn = None
		try:
			conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
			cur = conn.cursor()
			cur.execute(query, (owner, description, date_created, pickup_location, present_location, destination, price, status,))
			conn.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()

		#token here
		return jsonify({'Message': "Parcel created"}), 201

def connect():
	global conn
	global cur
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
	except (Exception, psycopg2.DatabaseError) as error:
		return jsonify({'message':'error', 'status':'failure'})


def execute_get_query(q):
	conn = None
	
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
		cur.execute(q)
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
			return cur

def validate_parcel_info(owner, description, pickup_location, destination):
	"""
		Function to validate parcel info. Making sure the required fields are filled in and correct
	"""

	if type(owner) != int: 
		return jsonify({'Message': 'Parcel owner must be identified by id (integer)'}), 400

	if description == "": 
		return jsonify({'Message': 'Description is empty'}), 400
	else:
		if len(description) > 124:
			return jsonify({'Message': 'Description should not be longer than 124 characters'}), 400

	if pickup_location == "": 
		return jsonify({'Message': 'Pickup_location is empty'}), 400
	else:
		if len(pickup_location) > 124:
			return jsonify({'Message': 'Pickup location should not be longer than 124 characters'}), 400

	if destination == "": 
		return jsonify({'Message': 'Destination is empty'}), 400
	else:
		if len(destination) > 124:
			return jsonify({'Message': 'Destination should not be longer than 124 characters'}), 400	


if __name__ == '__main__':
	app.run(debug=True)

