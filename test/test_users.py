import unittest
import os
import json
import pytest
from app import app

class APITestUsers(unittest.TestCase):

	login_user = {"username": "sanyu", "password": "pass123456"}
	signup_user = {"username": "sanyu", "email": "sanyu@gmail.com", "password": "pass123"}

	def setUp(self):
		self.app = app
		self.client = self.app.test_client()

	def get_token(self):
		"""
			Function for getting an access token
		"""
		response = self.client.post('/api/v1/auth/login', json=self.login_user)
		access_token = response.json['access_token']
		return access_token

	def test_signup(self):
		"""
			Test for signing a user up
		"""
		response = self.client.post('/api/v1/auth/signup', json=self.signup_user)
		#token = response.json['access_token']
		self.assertEqual(response.status_code, 400)
		self.assertIn("user already exists", str(response.json))

	def test_login(self):
		"""
			Test for logging a user in
		"""
		response = self.client.post('/api/v1/auth/login', json=self.login_user)
		token = response.json['access_token']
		self.assertEqual(response.status_code, 200)
		self.assertIn("user logged in", str(response.json))

	def test_get_users(self):
		"""
			Test for fetching all users
		"""
		token = self.get_token()
		response = self.client.get('/api/v1/users', content_type='application/json', headers={'Authorization': f'Bearer {token}'})
		self.assertEqual(response.status_code, 200)

	def test_get_user_parcels(self):
		"""
			Test for fetching all parcels of a specific user
		"""
		token = self.get_token()
		response = self.client.get('/api/v1/users/1/parcels', content_type='application/json', headers={'Authorization': f'Bearer {token}'})
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
