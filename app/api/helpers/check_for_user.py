from flask import Flask, request, jsonify
from app.models.models import DatabaseConnection

db = DatabaseConnection()

def check_in_db(user_email):
	query = """SELECT * FROM users WHERE email = %s;"""
	db.connect()
	db.cur.execute(query, (user_email,))
	db.connection.commit()
	result = db.cur.fetchall()
	if not result:
		db.connection.close()
		return True
	else:
		return jsonify({'message':'this user already exists', 'status':'failure'}), 400