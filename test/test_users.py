import unittest
import os
import json
import pytest
from test.test_base import BaseTest
from app import app

login_user = {"username": "sanyu", "password": "pass123"}
signup_user = {"username": "sanyu", "email": "sanyu@gmail.com", "password": "pass123"}
parcel = {"pickup_location": "Plot 1 Kampala Road", "destination": "Plot 5 Jinja Road", "description": "White envelope"}


class APITestUsers(BaseTest):
	def test_signup(self):
		"""
			Test for signing a user up
		"""
		response = self.client.post('/api/v1/auth/signup', json=signup_user)
		self.assertEqual(response.status_code, 201)
		self.assertIn("user signed up", str(response.json))

	def test_login(self):
		"""
			Test for logging a user in
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		response = self.client.post('/api/v1/auth/login', data=json.dumps(login_user), content_type='application/json')
		#token = result['access_token']
		self.assertEqual(response.status_code, 200)
		self.assertIn("user logged in", str(response.json))

	def test_get_user_parcels(self):
		"""
			Test for fetching all parcels of a specific user
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_token()
		self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		response = self.client.get('/api/v1/users/1/parcels', content_type='application/json', headers={'Authorization': token})
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
