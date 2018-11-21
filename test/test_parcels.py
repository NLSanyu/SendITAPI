import unittest
import os
import json
import pytest
from test.test_users import APITestUsers
from app.models.models import Tables
from app import app

user = APITestUsers()

class APITest(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.client = self.app.test_client()
		tables = Tables()
		tables.create_tables()

	def get_token(self):
		"""
			Function for getting an access token
		"""
		response = self.client.post('/api/v1/auth/login', json=user.login_user)
		access_token = response.json['access_token']
		return access_token

	def test_home(self):
		"""
			Test for fetching all parcel delivery orders
		"""
		response = self.client.get('/api/v1')
		self.assertEqual(response.status_code, 200)

	def test_get_parcels(self):
		"""
			Test for fetching all parcels
		"""
		token = self.get_token()
		response = self.client.get('/api/v1/parcels', content_type='application/json', headers={'Authorization': f'Bearer {token}'})
		self.assertEqual(response.status_code, 200)

	def test_get_one_parcel(self):
		"""
			Test for fetching one parcel
		"""
		token = self.get_token()
		response = self.client.get('/api/v1/parcels/1', content_type='application/json', headers={'Authorization': f'Bearer {token}'})
		self.assertEqual(response.status_code, 200)

	def test_cancel_parcel(self):
		"""
			Test for cancelling a parcel
		"""
		token = self.get_token()
		response = self.client.put('/api/v1/parcels/1/cancel', content_type='application/json', headers={'Authorization': f'Bearer {token}'})
		self.assertEqual(response.status_code, 400)
		self.assertIn("parcel non-existent", str(response.json))

	"""
	def test_change_parcel_dest(self):
		'''
			Test for changing a parcel's destination
		'''
		token = self.get_token()
		response = self.client.put('/api/v1/parcels/1/destination', content_type='application/json', json={"destination": "Kampala"}, headers={'Authorization': f'Bearer {token}'})
		self.assertEqual(response.status_code, 400)
		self.assertIn("parcel already delivered or cancelled", str(response.json))
	"""

if __name__ == '__main__':
    unittest.main()
