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
		self.login_user = {"username": "sanyu", "password": "pass123456"}
		self.signup_user = {"username": "sanyu", "email": "sanyu@gmail.com", "password": "pass123"}
		self.tables = Tables()
		self.tables.create_tables()
		
	"""
	def tearDown(self):
		self.tables.drop_tables()
	"""

	def get_token(self):
		"""
			Function for getting an access token
		"""
		response = self.client.post('/api/v1/auth/login', json=self.login_user)
		access_token = response.json['access_token']
		return access_token

	def get_admin_token(self):
		"""
			Function for getting an access token
		"""
		response = self.client.post('/api/v1/auth/login', json=self.admin_user)
		access_token = response.json['access_token']
		return access_token

if __name__ == '__main__':
    unittest.main()
