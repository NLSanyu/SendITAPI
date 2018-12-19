from flask import Flask, request, jsonify, make_response
from app.models.models import DatabaseConnection

def get_owner_name(owner_id):
	query = """SELECT * FROM users WHERE id = %s"""
	db = DatabaseConnection()
	db.connect()
	db.cur.execute(query, (owner_id,))
	result = db.cur.fetchall()
	for row in result:
		name = row[1]
	return name


def convert_to_dict(result):
	data_list = []
	for row in result:
		data = dict()
		data['parcel_id'] = row[0]
		data['owner_id'] = row[1]
		data['description'] = row[2]
		data['date_created'] = row[3]
		data['pickup_location'] = row[4]
		data['present_location'] = row[5]
		data['destination'] = row[6]
		data['weight'] = row[7]
		data['price'] = row[8]
		data['status'] = row[9]
		data_list.append(data)

	return data_list

