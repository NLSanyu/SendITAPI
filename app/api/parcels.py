import psycopg2
import flasgger
import datetime
from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app.models.models import DatabaseConnection
from app.api.helpers.parcel_helpers import get_owner_name, convert_to_dict
from app.api.helpers.validate_info import validate_key, validate
from app import app

db = DatabaseConnection()

@app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
@jwt_required
@flasgger.swag_from("./docs/get_a_parcel.yml")
def get_parcel(parcel_id):
	"""
		Function for API endpoint to fetch a specific parcel delivery order
	"""
	current_user = get_jwt_identity()

	query = """SELECT * FROM parcels WHERE id = %s;"""
	
	db.cur.execute(query, (parcel_id,))
	result = db.cur.fetchall()	
	if result:
		for row in result:
			if current_user['id'] != row[1]:
				return jsonify({'message': 'access denied', 'status': 'failure'}), 400

			parcels = convert_to_dict(result)
		return jsonify({'message': 'parcels retrieved', 'status': 'success', 'data': parcels}), 200
	else:
		return jsonify({'message': 'no parcel with this id', 'status': 'failure'}), 400


@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
@jwt_required
@flasgger.swag_from("./docs/change_parcel_destination.yml")
def cancel_order(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	current_user = get_jwt_identity()
	
	query = """SELECT * FROM parcels WHERE id = %s;"""
	db.cur.execute(query, (parcel_id,))
	result = db.cur.fetchall()
	if result:
		for row in result:
			id = row[1]
			name = get_owner_name(id)
			if current_user['username'] != name:
				return jsonify({'message': 'access denied', 'status': 'failure'}), 400
			if row[9] == "Delivered":
				return jsonify({'message': 'parcel already delivered', 'status': 'failure'}), 400
			else:
				query = """UPDATE parcels SET status = %s WHERE id = %s"""
				status = "Cancelled"
				db.cur.execute(query, (status, parcel_id,))
				return jsonify({'message': 'parcel cancelled', 'status': 'success'}), 200			
	else: 
		return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 400
		

@app.route('/api/v1/parcels/<int:parcel_id>/destination', methods=['PUT'])
@jwt_required
@flasgger.swag_from("./docs/cancel_a_parcel.yml")
def change_parcel_destination(parcel_id):
	"""
		Function for API endpoint to change the destination of a parcel delivery order
	"""
	current_user = get_jwt_identity()

	req = request.json
	req_keys = req.keys()
	if not validate_key(req_keys, 'destination'):
		return jsonify({'message': 'missing key: no destination entered', 'status': 'failure'}), 400
	else:
		destination = request.json['destination']
		if not validate(destination):
			return jsonify({'message': 'incorrect data entered: destination empty or incorrect length', 'status': 'failure'}), 400

	query = """SELECT * FROM parcels WHERE id = %s;"""
	db.cur.execute(query, (parcel_id,))
	result = db.cur.fetchall()
	if result:
		for row in result:
			id = row[1]
			name = get_owner_name(id)
			if current_user['username'] != name:
				return jsonify({'message': 'access denied', 'status': 'failure'}), 400
			if (row[9] == "Delivered" or row[9] == "Cancelled"):
				return jsonify({'message': 'parcel already delivered or cancelled', 'status': 'failure'}), 400
			else:
				query = """UPDATE parcels SET destination = %s WHERE id = %s"""
				db.cur.execute(query, (destination, parcel_id,))	
				return jsonify({'message': 'parcel destination changed', 'status': 'success'}), 200
	else: 
		return jsonify({'message': 'parcel non-existent', 'status': 'failure'}), 404


@app.route('/api/v1/parcels', methods=['POST'])
@jwt_required
@flasgger.swag_from("./docs/create_parcel.yml")
def create_parcel_order():
	"""
		Function for API endpoint to create a parcel delivery order
	"""
	current_user = get_jwt_identity()
	
	req = request.json
	req_keys = req.keys()
	if not(validate_key(req_keys, 'description') and validate_key(req_keys, 'pickup_location') and validate_key(req_keys, 'destination')):
		return jsonify({'message': 'incomplete data entered: key/keys missing', 'status': 'failure'}), 400
	else: 
		description = request.json['description']
		pickup_location = request.json['pickup_location'] 
		destination = request.json['destination'] 

	date_created = datetime.datetime.now()
	present_location = request.json['pickup_location']
	price = 'UGX 3000'
	weight = ' '
	status = 'Pending'
	owner_id = current_user['id']

	if not(validate(description) and validate(pickup_location) and validate(destination)):
		return jsonify({'message': 'parcel not created: invalid info', 'status': 'failure'}), 400
	else:
		query = """INSERT INTO parcels (owner_id, description, date_created, pickup_location, present_location, destination, weight, price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
		db.cur.execute(query, (owner_id, description, date_created, pickup_location, present_location, destination, weight, price, status,))
		return jsonify({'message': 'parcel created', 'status': 'success'}), 201

