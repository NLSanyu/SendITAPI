from flask import Flask, request, jsonify, abort, make_response
import re

def validate_email(email):
	pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
	return re.match(pattern, email)



