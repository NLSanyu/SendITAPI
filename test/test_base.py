import unittest
import os
import json
import pytest
from app.models.models import Tables
from app import app


class BaseTest(unittest.TestCase):

	def setUp(self):
		self.app = app
		self.client = self.app.test_client()
		self.parcel = {"owner": "1", "pickup_location": "Plot 1 Kampala Road", "destination": "Plot 5 Jinja Road", "description": "White envelope"}
		self.admin_user = {"username": "admin", "email": "adm@gmail.com", "password": "admin"}
		self.login_user = {"username": "sanyu", "password": "pass123"}
		self.signup_user = {"username": "sanyu", "email": "sanyu@gmail.com", "password": "pass123"}
		self.tables = Tables()
		self.tables.create_tables()
		
	def tearDown(self):
		self.tables.drop_tables()

	def get_token(self):
		"""
			Function for getting an access token
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup_user), content_type='application/json')
		response = self.client.post('/api/v1/auth/login', data=json.dumps(self.login_user), content_type='application/json')
		resp = json.loads(response.data.decode())
		return 'Bearer ' + resp['access_token']

	def get_admin_token(self):
		"""
			Function for getting an admin access token
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(self.admin_user), content_type='application/json')
		response = self.client.post('/api/v1/auth/login', data=json.dumps(self.admin_user), content_type='application/json')
		resp = json.loads(response.data.decode())
		return 'Bearer ' + resp['access_token']

if __name__ == '__main__':
    unittest.main()
