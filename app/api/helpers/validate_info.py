from flask import Flask, request, jsonify, abort, make_response

def validate_key(req_keys, key_name):
	return key_name in req_keys

def validate(info):
	"""
		Function to validate user inputs. Making sure the required fields are filled in and correct
	"""

	if info == "": 
		return False
	else:
		if len(info) < 5 or len(info) > 32:
			return False
		else:
			return True