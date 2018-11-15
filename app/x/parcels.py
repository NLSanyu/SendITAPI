import datetime
from flask import Flask, request, jsonify, abort, make_response
from app import app


parcels = [
	{
		'id': 1,
		'owner': 0,
		'description': 'Brown Box tied with blue string',
		'date_created': '28-10-2018',
		'pickup_location': 'Plot 55 Luwum Street',
		'present_location': 'Plot 305 Nakesero Road',
		'destination': 'Plot 305 Nakesero Road',
		'price': 'shs 4,000',
		'status': 'Delivered'
	},
	{
		'id': 2,
		'owner': 1,
		'description': 'White A4 size envelope',
		'date_created': '30-10-2018',
		'pickup_location': 'Plot 49 Ntinda Rd',
		'present_location': 'Kampala Road',
		'destination': 'Plot 3 Wampeewo Avenue',
		'price': 'shs 8,000',
		'status': 'In Transit'
	},
	{
		'id': 2,
		'owner': 2,
		'description': 'Red and black gift bag',
		'date_created': '31-10-2018',
		'pickup_location': 'Plot 11 Colville Street',
		'present_location': 'Shop no.25 Oasis Mall',
		'destination': 'Shop no.25 Oasis Mall',
		'price': 'shs 3,000',
		'status': 'Delivered'
	},
	{
		'id': 4,
		'owner': 2,
		'description': 'Brown box 10cm x 15cm',
		'date_created': '2-11-2018',
		'pickup_location': 'Plot 11 Colville Street',
		'present_location': 'Parliamentary Avenue',
		'destination': 'Shop no.25 Oasis Mall',
		'price': 'shs 3,000',
		'status': 'In Transit'
	}
]

@app.route('/api/v1/parcels', methods=['GET'])
def get_all_parcels():
	"""
		Function for API endpoint to fetch all parcel delivery orders
	"""
	if len(parcels) == 0:
		abort(404, 'Error: No parcels delivery orders made yet')
	return jsonify({'parcels': parcels}), 200

@app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
def get_parcel(parcel_id):
	"""
		Function for API endpoint to fetch a specific parcel delivery order
	"""
	parcel = [parcel for parcel in parcels if parcel['id'] == parcel_id]
	if len(parcel) == 0:
		abort(404, 'Error: No parcel with this id')
	return jsonify({'parcel': parcel[0]}), 200

@app.route('/api/v1/parcels/<int:parcel_id>/cancel', methods=['PUT'])
def cancel_order(parcel_id):
	"""
		Function for API endpoint to cancel a parcel delivery order
	"""
	parcel = [parcel for parcel in parcels if parcel['id'] == parcel_id]
	if len(parcel) == 0:
		abort(404, 'Error: No parcel with this id')
	if parcel[0]['status'] == 'Delivered':
		abort(403, 'Error: Status cannot be chnaged. Parcel is already delivered')
	else:
		parcel[0]['status'] = 'Cancelled'
		return jsonify({'parcel': parcel[0]}), 200

@app.route('/api/v1/parcels', methods=['POST'])
def create_order():
	"""
		Function for API endpoint to create a parcel delivery order
	"""
	
	date = datetime.datetime.now()
	date_string = str(date.day) + "-" + str(date.month) + "-" + str(date.year)

	parcel = {
		'id' : parcels[-1]['id'] + 1,
		'owner': request.json['owner'],
		'description': parcels[-1]['id'] + 1,
		'date_created': date_string,
		'pickup_location': request.json['pickup_location'],
		'present_location': request.json['pickup_location'],
		'destination': request.json['destination'],
		'price': ' ',
		'status': 'Not picked up'
	}

	parcels.append(parcel)
	return jsonify({'parcels': parcels}), 201

if __name__ == '__main__':
	app.run(debug=True)

