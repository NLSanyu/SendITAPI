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

	query = """SELECT * FROM users ORDER BY id DESC;"""
	db.cur.execute(query)
	result = db.cur.fetchall()
	if result:
		users = convert_users_to_dict(result)
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

	query = """SELECT * FROM parcels ORDER BY id DESC;"""
	db.cur.execute(query)
	result = db.cur.fetchall()
	if result:
		parcels = convert_to_dict(result)
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

	all_status = ["Delivered", "Cancelled", "Pending", "In Transit"]
	if status in all_status:
		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.cur.execute(query, (parcel_id,))
		result = db.cur.fetchall()
		if result:
			for row in result:
				if row[9] == "Delivered":
					return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
				else:
					query = """UPDATE parcels SET status = %s WHERE id = %s"""
					db.cur.execute(query, (status, parcel_id,))
					return jsonify({'message': 'parcel status updated', 'status' :'success'}), 200	
		else: 	
			db.cur.close()
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
	req_keys = req.keys()
	if not validate_key(req_keys, 'location'):
		return jsonify({'message': 'missing key: no location entered', 'status': 'failure'}), 400
	else:
		location = request.json['location']
		if not validate(location):
			return jsonify({'message': 'incorrect data entered: location empty or incorrect length', 'status': 'failure'}), 400

		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.cur.execute(query, (parcel_id,))
		result = db.cur.fetchall()
		if result:
			for row in result:
				if row[9] == "Delivered":
					return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
				else:
					query = """UPDATE parcels SET present_location = %s WHERE id = %s"""
					db.cur.execute(query, (location, parcel_id,))	
					return jsonify({'message':'parcel present location updated', 'status':'success'}), 200
		else: 
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400	


@app.route('/api/v1/parcels/<int:parcel_id>/price', methods=['PUT'])
@jwt_required
def edit_parcel_price(parcel_id):
	"""
		Function for API endpoint to enter/edit the price of a parcel delivery order
	"""
	current_user = get_jwt_identity()

	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400
	
	req = request.json
	req_keys = req.keys()
	if not validate_key(req_keys, 'price'):
		return jsonify({'message': 'missing key: no price entered', 'status': 'failure'}), 400
	else:
		price = request.json['price']
		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.cur.execute(query, (parcel_id,))
		result = db.cur.fetchall()
		if result:
			for row in result:
				if row[9] == "Cancelled":
					return jsonify({'message': 'parcel already cancelled', 'status': 'failure'}), 400
				else:
					query = """UPDATE parcels SET price = %s WHERE id = %s"""
					db.cur.execute(query, (price, parcel_id,))
					return jsonify({'message': 'parcel price edited', 'status' :'success'}), 200	
		else: 	
			db.cur.close()
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400


@app.route('/api/v1/parcels/<int:parcel_id>/weight', methods=['PUT'])
@jwt_required
def edit_parcel_weight(parcel_id):
	"""
		Function for API endpoint to enter/edit the weight of a parcel delivery order
	"""
	current_user = get_jwt_identity()

	if current_user['username'] != "admin" and current_user['password'] != "admin":
		return jsonify({'message': 'access denied', 'status': 'failure'}), 400
	
	req = request.json
	req_keys = req.keys()
	if not validate_key(req_keys, 'weight'):
		return jsonify({'message': 'missing key: no weight entered', 'status': 'failure'}), 400
	else:
		weight = request.json['weight']
		query = """SELECT * FROM parcels WHERE id = %s;"""
		db.cur.execute(query, (parcel_id,))
		result = db.cur.fetchall()
		if result:
			for row in result:
				if row[9] == "Cancelled":
					return jsonify({'message': 'parcel already cancelled', 'status': 'failure'}), 400
				else:
					query = """UPDATE parcels SET weight = %s WHERE id = %s"""
					db.cur.execute(query, (weight, parcel_id,))
					return jsonify({'message': 'parcel weight edited', 'status' :'success'}), 200	
		else: 	
			db.cur.close()
			return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400
	