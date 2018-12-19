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
		data['full_name'] = row[1]
		data['username'] = row[2]
		data['email'] = row[3]
		data['phone_number'] = row[4]
		data['password_hash'] = row[5]
		data_list.append(data)

	return data_list

def convert_one_user_to_dict(row):
	data = dict()
	data['user_id'] = row[0]
	data['full_name'] = row[1]
	data['username'] = row[2]
	data['email'] = row[3]
	data['phone_number'] = row[4]
		
	return data

