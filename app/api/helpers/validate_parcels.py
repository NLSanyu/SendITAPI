from flask import Flask, request, jsonify, make_response

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
