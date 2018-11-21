import psycopg2
import datetime
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from app import app

query = ""
db = DatabaseConnection()

@app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'])
@jwt_required
def change_parcel_status(parcel_id):
	"""
		Function for API endpoint to change the status a parcel delivery order
	"""
	current_user = get_jwt_identity()

	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400

	all_status = ["Delivered", "Cancelled", "New", "In Transit", "Not picked up"]
	req = request.json
	if 'status' not in req.keys():
		return jsonify({'message': 'no status entered', 'status' :'failure'}), 400

	status = request.json['status']
	if status in all_status:
		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.connect()
		db.cur.execute(query, (parcel_id,))
		db.connection.commit()
		result = db.cur.fetchall()
		if result:
			for row in result:
				if row[8] == "Delivered":
					return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
				else:
					query = """UPDATE parcels SET status = %s WHERE id = %s"""
					db.cur.execute(query, (status, parcel_id,))
					db.cur.close()
					db.connection.close()
					return jsonify({'message': 'parcel status updated', 'status' :'success'}), 200	
		else: 	
			db.cur.close()
			db.connection.close()
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400
	else:
		return jsonify({'message': 'incorrect status', 'status': 'failure'}), 400	


@app.route('/api/v1/parcels/<int:parcel_id>/presentLocation', methods=['PUT'])
@jwt_required
def change_parcel_location(parcel_id):
	"""
		Function for API endpoint to change the present location of a parcel delivery order
	"""
	current_user = get_jwt_identity()
	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400

	req = request.json
	if 'location' in req.keys():
		location = request.json['location']
		if location == "": 
			return jsonify({'message': 'present location is empty', 'status': 'failure'}), 400
		else:
			if len(location) > 124:
				return jsonify({'message':'present location should not be longer than 124 characters', 'status':'failure'}), 400

		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.connect()
		
		db.cur.execute(query, (parcel_id,))
		db.connection.commit()
		result = db.cur.fetchall()
		if result:
			for row in result:
				if row[8] == "Delivered":
					return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
				else:
					query = """UPDATE parcels SET present_location = %s WHERE id = %s"""
					db.cur.execute(query, (location, parcel_id,))	
					return jsonify({'message':'parcel present location updated', 'status':'success'}), 200
		else: 
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400	
	else:
		return jsonify({'message': 'no location entered', 'status': 'failure'}), 400	
