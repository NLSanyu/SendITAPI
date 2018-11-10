from flask import render_template, flash, redirect
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

parcels = [
	{
		'id': 0,
		'owner': 'EddieKM',
		'description': 'Brown Box tied with blue string',
		'date_created': '28-10-2018',
		'pickup_location': 'Plot 55 Luwum Street',
		'present_location': 'Plot 305 Nakesero Road',
		'destination': 'Plot 305 Nakesero Road',
		'price': 'shs 4,000',
		'status': 'Delivered'
	},
	{
		'id': 1,
		'owner': 'Xtine4',
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
		'owner': 'MRichyz',
		'description': 'Red and black gift bag',
		'date_created': '31-10-2018',
		'pickup_location': 'Plot 11 Colville Street',
		'present_location': 'Shop no.25 Oasis Mall',
		'destination': 'Shop no.25 Oasis Mall',
		'price': 'shs 3,000',
		'status': 'Delivered'
	},
	{
		'id': 3,
		'owner': 'MRichyz',
		'description': 'Brown box 10cm x 15cm',
		'date_created': '2-11-2018',
		'pickup_location': 'Plot 11 Colville Street',
		'present_location': 'Parliamentary Avenue',
		'destination': 'Shop no.25 Oasis Mall',
		'price': 'shs 3,000',
		'status': 'In Transit'
	}
]

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
	return render_template('sign_in.html', title='Sign In')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
	return render_template('sign_up.html', title='Sign Up')

@app.route('/profile')
def profile():
	return render_template('profile.html', title='Profile', users=users)

@app.route('/parcels')
def parcels():
	return render_template('parcels.html', parcels=parcels)

@app.route('/create_parcel')
def create_parcel():
	return render_template('create_parcel.html', title='Create Parcel Delivery Order')

@app.route('/admin_sign_in', methods=['GET', 'POST'])
def admin_sign_in():
	return render_template('admin_sign_in.html', title='Administrator Sign In')

@app.route('/admin_page')
def admin_page():
	return render_template('admin_page.html', title='Admin', parcels=parcels)

######     API      #########

#fetch all parcel delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
def get_all_parcels():
	return jsonify({'parcels': parcels})

#fetch a specific parcel delivery order
@app.route('/api/v1/parcels/<int:parcel_id>', methods=['GET'])
def get_parcel(parcel_id):
	parcel = [parcel for parcel in parcels if parcel['id'] == parcel_id]
	if len(parcel) == 0:
		abort(404)
	return jsonify({'parcel': parcel[0]})

#fetch all parcel delivery orders by a specific user
@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
def get_user_parcel(user_id):
	parcel = [parcel for parcel in parcels if parcel['owner'] == user_id]
	if len(parcel) == 0:
		abort(404)
	return jsonify({'parcels': parcel})

#cancel a specific parcel delivery order
@app.route('/api/v1/parcels/<parcel_id>/cancel', methods=['PUT'])
def cancel_order():
	parcel = [parcel for parcel in parcels if parcel['id'] == parcel_id]
	if len(parcel) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if parcel[0]['status'] == 'Delivered':
		abort(403)
	else:
		parcel[0]['status'] = 'Cancelled'
		return jsonify({'parcel': parcel[0]})

#create a parcel delivery order
@app.route('/api/v1/parcels', methods=['POST'])
def create_order():
	if not request.json or not ('pickup location' and 'description' and 'destination' and 'owner' in request.json):
		abort(400)

	date = datetime.datetime.now()
	date_string = date.day + "-" + date.month + "-" + date.year

	parcel = {
		'id' : parcels[-1]['id'] + 1,
		'owner': request.json['owner'],
		'description': tasks[-1]['id'] + 1,
		'date created': date_string,
		'pickup location': request.json['pickup location'],
		'present location': request.json['pickup location'],
		'destination': request.json['destination'],
		'price': ' ',
		'status': 'Not picked up'
	}
	parcels.append(parcel)
	return jsonify({'parcel': parce}), 201





if __name__ == '__main__':
	app.run(debug=True)

