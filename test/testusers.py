import unittest
import os
import json
import pytest
from app import app

class APITestUsers(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.client = self.app.test_client()

	def test_signup(self):
		user = {"username": "lydia", "email": "lydia@gmail.com", "password": "pass123"}
		response = self.client.post('/api/v1/auth/signup', json=user)
		self.assertEqual(response.status_code, 201)
		#self.assertIn(str(response), "user created")

	def test_login(self):
		user = {"username": "lydia", "email": "lydia@gmail.com", "password": "pass123"}
		response = self.client.post('/api/v1/auth/login', json=user)
		self.assertEqual(response.status_code, 201)
		#self.assertIn(str(response), "user created")

	def test_fetch_users(self):
		"""
			Test for fetching all users
		"""
		response = self.client.get('/api/v1/users', content_type='application/json')
		self.assertEqual(response.status_code, 200)

	def test_fetch_user_parcels(self):
		"""
			Test for fetching all parcels of a specific user
		"""
		response = self.client.get('/api/v1/users/2/parcels', content_type='application/json')
		self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
