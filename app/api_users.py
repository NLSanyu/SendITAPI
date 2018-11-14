import datetime
from app import api_parcels
from flask import Flask, request, jsonify, abort, render_template
from app import app


users = [
	{
		'id': 0,
		'username': 'EddieKM',
		'email': 'eddiekm@gmail.com',
		'password': '12345',
		'no_of_orders': 1,
		'no_delivered': 1,
		'no_in_transit': 0,
		'frequent_locations': ['Plot 55 Luwum Street']
	},
	{
		'id': 1,
		'username': 'Xtine4',
		'email': 'xtine4@gmail.com',
		'password': '23456',
		'no_of_orders': 1,
		'no_delivered': 0,
		'no_in_transit': 1,
		'frequent_locations': ['Plot 49 Ntinda Rd']
	},
	{
		'id': 2,
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
	return "<p>SendIT API</p>"

#fetch all users
@app.route('/api/v1/users', methods=['GET'])
def get_all_users():
	return jsonify(users), 200

#fetch all parcel delivery orders by a specific user
@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
def get_user_parcel(user_id):
	parcel = [parcel for parcel in api_parcels.parcels if parcel['owner'] == user_id]
	if len(parcel) == 0:
		abort(404)
	return jsonify({'parcels': parcel}), 200


if __name__ == '__main__':
	app.run(debug=True)
