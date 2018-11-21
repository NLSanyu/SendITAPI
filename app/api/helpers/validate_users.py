from flask import Flask, request, jsonify, make_response
import re


def validate_user_info(username, email, password, signup):
	"""
		Function to validate user inputs. Making sure the required fields are filled in and correct
	"""

	if username == "": 
		return jsonify({'message': 'username is empty', 'status': 'failure'}), 400
	else:
		if len(username) > 32:
			return jsonify({'message': 'username should not longer than 32 characters', 'status': 'failure'}), 400	

	if password == "": 
		return jsonify({'message': 'password is empty', 'status': 'failure'}), 400
	else:
		if len(password) < 6:
			return jsonify({'message': 'password should be longer than 6 characters', 'status': 'failure'}), 400	

	if signup:
		if email == "": 
			return jsonify({'message': 'email address is empty', 'status': 'failure'}), 400
		else:
			pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
			if not re.match(pattern, email):
				return jsonify({'message': 'enter a valid email', 'status': 'failure'}), 400

	return True


