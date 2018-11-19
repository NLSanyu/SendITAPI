import psycopg2
import datetime
from flask import Flask, request, jsonify, abort, make_response
from app import app

query = ""
conn = None

@app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'])
def change_parcel_status(parcel_id):
	"""
		Function for API endpoint to change the status a parcel delivery order
	"""
	all_status = ["Delivered", "Cancel", "New", "In Transit", "Not picked up"]
	status = request.json('status')
	if status in all_status:
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
	else:
		abort(400, 'Incorrect status')


@app.route('/api/v1/parcels/<int:parcel_id>/presentLocation', methods=['PUT'])
def change_parcel_location(parcel_id):
	"""
		Function for API endpoint to change the present location of a parcel delivery order
	"""
	location = request.json['present_location']
	if location == "": 
		return jsonify({'Message': 'Present location is empty'}), 400
	else:
		if len(location) > 124:
			return jsonify({'Message': 'Present location should not be longer than 124 characters'}), 400

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
					query = """UPDATE parcels SET present_location = %s WHERE id = %s"""
					cur = conn.cursor()
					cur.execute(query, (location, parcel_id, ))	
		else: 
			abort(404, 'Parcel non-existent')	
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()