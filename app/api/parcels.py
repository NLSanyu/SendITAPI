import psycopg2
import datetime
from flask import Flask, request, jsonify, abort, make_response
from app import app

query = ""
status = "Cancelled"
conn = None


@app.route('/api/v1/parcels', methods=['GET'])
def get_all_parcels():
	"""
		Function for API endpoint to fetch all parcel delivery orders
	"""
	query = """SELECT * FROM parcels;"""
	connect()
	res = execute_get_query(query)
	if res:
		parcels = res.fetchall
		if parcels:
			return jsonify({'parcels': 'Parcels'}), 200
		#return jsonify({'parcels': parcels}), 200
	else:
		abort(404, 'No parcels')


@app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
def get_parcel(parcel_id):
	"""
		Function for API endpoint to fetch a specific parcel delivery order
	"""
	query = """SELECT * FROM parcels WHERE id=%d;"""
	if type(parcel_id) != int:
		return jsonify({'Message': "Id should be an integer"}), 400
	else:
		try:
			conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
			cur = conn.cursor()
			cur.execute(query, (parcel_id,))
			conn.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()

	res = cur.fetch()	
	if res:
		return jsonify({'parcel': 'parcel'}), 200
	else:
		abort(404, "No parcel with this id")


@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
def cancel_order(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	query = """SELECT * FROM parcels WHERE id=%d AND status <> %s;"""
	conn = None
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
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)


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

