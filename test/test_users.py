import unittest
import os
import json
import pytest
from test.test_base import BaseTest
from app import app

login_user = {"username": "sanyu", "password": "pass123456"}
signup_user = {"username": "sanyu", "email": "sanyu@gmail.com", "password": "pass123"}

class APITestUsers(BaseTest):
	def test_signup(self):
		"""
			Test for signing a user up
		"""
		response = self.client.post('/api/v1/auth/signup', json=signup_user)
		#token = response.json['access_token']
		self.assertEqual(response.status_code, 201)
		self.assertIn("user signed up", str(response.json))

	def test_login(self):
		"""
			Test for logging a user in
		"""
		response = self.client.post('/api/v1/auth/login', json=login_user)
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
