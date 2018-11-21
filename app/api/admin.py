import psycopg2
import datetime
from flask import Flask, request, jsonify, make_response
from app.models.models import DatabaseConnection
from app import app

query = ""
db = DatabaseConnection()

@app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'])
def change_parcel_status(parcel_id):
	"""
		Function for API endpoint to change the status a parcel delivery order
	"""
	all_status = ["Delivered", "Cancel", "New", "In Transit", "Not picked up"]
	req = request.json
	if 'status' not in req.keys():
		return jsonify({'message':'no status entered', 'status':'failure'}), 400

	status = request.json['status']
	if status in all_status:
		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.connect()
		db.cur.execute(query, (parcel_id,))
		db.connection.commit()
		result = db.cur.fetchall()
		if result != None:
			for row in db.cur:
				if row[8] == "Delivered":
					return jsonify({'message':'parcel already delivered', 'status':'failure'}), 400
				else:
					query = """UPDATE parcels SET status = %s WHERE id = %s"""
					db.cur.execute(query, (status, parcel_id, ))
					db.cur.close()
					db.connection.close()
					return jsonify({'message':'parcel status updated', 'status':'success'}), 400	
		else: 	
			db.cur.close()
			db.connection.close()
			return jsonify({'message':'parcel non-existent', 'status':'failure'}), 400
	else:
		return jsonify({'message':'incorrect status', 'status':'failure'}), 400	


@app.route('/api/v1/parcels/<int:parcel_id>/presentLocation', methods=['PUT'])
def change_parcel_location(parcel_id):
	"""
		Function for API endpoint to change the present location of a parcel delivery order
	"""
	req = request.json
	if 'location' in req.keys():
		location = request.json['present_location']
		if location == "": 
			return jsonify({'message':'present location is empty', 'status':'failure'}), 400
		else:
			if len(location) > 124:
				return jsonify({'message':'present location should not be longer than 124 characters', 'status':'failure'}), 400

		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.connect()
		
		db.cur.execute(query, (parcel_id,))
		db.connection.commit()
		if db.cur.fetchall:
			for row in db.cur:
				if row[9] == "Delivered":
					return jsonify({'message':'parcel already delivered', 'status':'failure'}), 400
				else:
					query = """UPDATE parcels SET present_location = %s WHERE id = %s"""
					db.cur.execute(query, (location, parcel_id, ))	
					return jsonify({'message':'parcel present location updated', 'status':'success'}), 400
		else: 
			return jsonify({'message':'parcel non-existent', 'status':'failure'}), 400	
	else:
		return jsonify({'message':'no location entered', 'status':'failure'}), 400	


def connect_to_db():
	global db
	db = DatabaseConnection()