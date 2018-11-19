import psycopg2
import datetime
from flask import Flask, request, jsonify, abort, make_response
from app import app

query = ""
conn = None

@app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'])
def change_parcel_status(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	query = """SELECT * FROM parcels WHERE id=%d AND status <> %s;"""
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
def change_order_destination(parcel_id):
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
	conn = None
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