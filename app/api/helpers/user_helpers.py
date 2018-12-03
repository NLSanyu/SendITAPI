from flask import Flask, request, jsonify, abort, make_response
import re

def validate_email(email):
	pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
	return re.match(pattern, email)

def convert_users_to_dict(result):
	data_list = []
	for row in result:
		data = dict()
		data['user_id'] = row[0]
		data['username'] = row[1]
		data['email'] = row[2]
		data['phone_number'] = row[3]
		data['password_hash'] = row[4]
		data['orders'] = row[5]
		data['delivered'] = row[6]
		data['in_transit'] = row[7]
		data_list.append(data)

	return data_list

def convert_one_user_to_dict(result):
	data_list = []
	for row in result:
		data = dict()
		data['username'] = row[1]
		data['email'] = row[2]
		data['phone_number'] = row[3]
		data['orders'] = row[5]
		data['delivered'] = row[6]
		data['in_transit'] = row[7]
		data_list.append(data)
		
	return data_list

