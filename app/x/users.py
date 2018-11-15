import datetime
from app import api_parcels
from flask import Flask, request, jsonify, abort, make_response
from app import app


users = [
	{
		'id': 1,
		'username': 'EddieKM',
		'email': 'eddiekm@gmail.com',
		'password': '12345',
		'no_of_orders': 1,
		'no_delivered': 1,
		'no_in_transit': 0,
		'frequent_locations': ['Plot 55 Luwum Street']
	},
	{
		'id': 2,
		'username': 'Xtine4',
		'email': 'xtine4@gmail.com',
		'password': '23456',
		'no_of_orders': 1,
		'no_delivered': 0,
		'no_in_transit': 1,
		'frequent_locations': ['Plot 49 Ntinda Rd']
	},
	{
		'id': 3,
		'username': 'MRichyz',
		'email': 'mrichyz@gmail.com',
		'password': '34567',
		'no_of_orders': 2,
		'no_delivered': 1,
		'no_in_transit': 1,
		'frequent_locations': ['Plot 11 Colville Street', 'Shop no.25 Oasis Mall']
	}
]

#api
@app.route('/api/v1', methods=['GET'])
def api_home():
	"""
		Function for API home
	"""
	return "<p>SendIT API</p>"

@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
	"""
		Function for API endpoint to fetch all users
	"""
	if len(users) == 0:
		abort(404, 'Error: No users registered yet')
	return jsonify(users), 200

@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
def get_user_parcel(user_id):
	"""
		Function for API endpoint to fetch all parcel delivery orders by a specific user
	"""
	parcel = [parcel for parcel in api_parcels.parcels if parcel['owner'] == user_id]
	if len(parcel) == 0:
		abort(404, 'Error: No parcels created by this user yet')
	return jsonify({'parcels': parcel}), 200


if __name__ == '__main__':
	app.run(debug=True)
