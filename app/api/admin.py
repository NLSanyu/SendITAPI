import psycopg2
import datetime
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.api.helpers.validate_info import validate_key, validate
from app.api.helpers.parcel_helpers import get_owner_name, convert_to_dict
from app.api.helpers.user_helpers import convert_users_to_dict
from app.models.models import DatabaseConnection
from app import app

query = ""
db = DatabaseConnection()

@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def get_all_users():
	"""
		Function for API endpoint to fetch all users
	"""
	current_user = get_jwt_identity()
	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400

	query = """SELECT * FROM users;"""
	db.connect()
	db.cur.execute(query)
	db.connection.commit()
	result = db.cur.fetchall()
	if result:
		users = convert_users_to_dict(result)
		db.connection.close()
		return jsonify({'message': 'users retrieved', 'status': 'success', 'data': users}), 200
	else:
		return jsonify({'message':'no users signed up yet', 'status':'failure'}), 200


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
		parcels = convert_to_dict(result)
		db.connection.close()
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': parcels}), 200
	else:
		return jsonify({'message':'no parcels created yet', 'status':'success'}), 200
	

@app.route('/api/v1/parcels/<int:parcel_id>/status', methods=['PUT'])
@jwt_required
def change_parcel_status(parcel_id):
	"""
		Function for API endpoint to change the status a parcel delivery order
	"""
	current_user = get_jwt_identity()

	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400
	
	req = request.json
	req_keys = req.keys()
	if not validate_key(req_keys, 'status'):
		return jsonify({'message': 'missing key: no status entered', 'status': 'failure'}), 400
	else:
		status = request.json['status']
		if not validate(status):
			return jsonify({'message': 'incorrect data entered: status empty or incorrect length', 'status': 'failure'}), 400

	all_status = ["Delivered", "Cancelled", "New", "In Transit", "Not picked up"]
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
	#re-test this route
	current_user = get_jwt_identity()
	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400

	req = request.json
	req_keys = req.keys()
	if not validate_key(req_keys, 'location'):
		return jsonify({'message': 'missing key: no location entered', 'status': 'failure'}), 400
	else:
		location = request.json['location']
		if not validate(location):
			return jsonify({'message': 'incorrect data entered: location empty or incorrect length', 'status': 'failure'}), 400

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