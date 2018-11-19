import psycopg2
import datetime, re
from app.api import parcels
from app.api.parcels import execute_get_query
from flask import Flask, request, jsonify, abort, make_response
from app import app

conn = None

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
	query = "SELECT * FROM users;"
	
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()
		result = cur.fetchall
		users_dict = dict()
		for row in result:
			users_dict['id'] = row[0]
			users_dict['username'] = row[1]
		return jsonify({'users': users_dict}), 200
		#else:
			#abort(404, 'No users yet')
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		return jsonify({"Error": str(error)}), 400
	finally:
		if conn is not None:
			cur.close()
			conn.close()
			
	
@app.route('/api/v1/users/<int:user_id>/parcels', methods=['GET'])
def get_user_parcel(user_id):
	"""
		Function for API endpoint to fetch all parcel delivery orders by a specific user
	"""

	query = """SELECT * FROM parcels WHERE owner = %d;"""
	conn = None
	try:
		conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
		cur = conn.cursor()
		cur.execute(query, (user_id,))
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

	if cur.fetchall():
		return jsonify({'Message': "Parcels for user"}), 200
	else:
		abort(400, "User or parcels not found")

@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
	"""
		Function for API endpoint to log a user in
	"""
	username = request.json['username'] 
	password = request.json['passwor'] 
	email=""
	if validate_user_info(username, email, password, False):
		query = """SELECT * FROM users WHERE username = %s AND passwor=%s;"""
		conn = None
		try:
			conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
			cur = conn.cursor()
			cur.execute(query, (username, password,))
			conn.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()

		if cur.fetchall():
			return jsonify({'Message': "User logged in"}), 200
			#token here


@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
	"""
		Function for API endpoint to sign a user up
	"""

	username = request.json['username'] 
	email = request.json['email']  
	password = request.json['passwor'] 
	if validate_user_info(username, email, password, True):
		query = """ INSERT INTO users (username, email, passwor) VALUES (%s, %s, %s)"""
		conn = None
		try:
			conn = psycopg2.connect(database="testdb", user = "postgres", password = "memine", host = "localhost", port = "5432")
			cur = conn.cursor()
			cur.execute(query, (username, email, password,))
			conn.commit()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()

		#get token here?

		return jsonify({'Message': "User created"}), 201



def validate_user_info(username, email, password, signup):
	"""
		Function to validate user inputs. Making sure the required fields are filled in and correct
	"""

	if username == "": 
		return jsonify({'Message': 'Username is empty'}), 400
	else:
		if len(username) > 32:
			return jsonify({'Message': 'Username should not longer than 32 characters'}), 400	

	if password == "": 
		return jsonify({'Message': 'Password is empty'}), 400
	else:
		if len(password) < 6:
			return jsonify({'Message': 'Password should be longer than 6 characters'}), 400	

	if signup:
		if email == "": 
			return jsonify({'Message': 'Email address is empty'}), 400
		else:
			pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
			if not re.match(pattern, email):
				return jsonify({'Message': 'Enter a valid email'}), 400

