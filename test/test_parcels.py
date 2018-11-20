import unittest
import os
import json
import pytest
from test.base import BaseTestCase
from app import app

class APITest(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.client = self.app.test_client()

	def test_home(self):
		"""
			Test for fetching all parcel delivery orders
		"""
		response = self.client.get('/api/v1')
		self.assertEqual(response.status_code, 200)

	

if __name__ == '__main__':
    unittest.main()
