from flask import Flask, request, jsonify, abort, make_response
import re


def validate_user_info(info):
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

def validate_email(email):
	pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
	return re.match(pattern, email)



