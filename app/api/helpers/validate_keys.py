from flask import Flask, request, jsonify, abort, make_response

def validate_key(req_keys, key_name):
	return key_name in req_keys

