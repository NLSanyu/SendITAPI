import unittest
import os
import json
import pytest
from test.base import BaseTestCase
from app import app

new_parcel = {
	'id': 4,
	'owner': 2,
	'description': 'Green box',
	'date_created': '4-11-2018',
	'pickup_location': 'Plot 11 Colville Street',
	'present_location': 'Shop no.25 Oasis Mall',
	'destination': 'Shop no.25 Oasis Mall',
	'price': 'shs 3,000',
	'status': 'Not picked up'
}

class APITest(BaseTestCase):
	def setUp(self):
		self.app = super().create_app()
		self.client = self.app.test_client()
		self.new_parcel = {
			'id': 4,
			'owner': 2,
			'description': 'Green box',
			'date_created': '4-11-2018',
			'pickup_location': 'Plot 11 Colville Street',
			'present_location': 'Shop no.25 Oasis Mall',
			'destination': 'Shop no.25 Oasis Mall',
			'price': 'shs 3,000',
			'status': 'New'
		}

	def test_fetch_users(self):
		response = self.client.get('/api/v1/users', content_type='application/json')
		self.assertEqual(response.status_code, 200)

	def test_fetch_parcels(self):
		response = self.client.get('/api/v1/parcels', content_type='application/json')
		self.assertEqual(response.status_code, 200)

	def test_fetch_a_parcel(self):
		response = self.client.get('/api/v1/parcels/3', content_type='application/json')
		self.assertEqual(response.status_code, 200)

	def test_fetch_a_user_parcel(self):
		response = self.client.get('/api/v1/users/2/parcels', content_type='application/json')
		self.assertEqual(response.status_code, 200)

	def test_create_parcel(self):
		response = self.client.post('/api/v1/parcels', json=new_parcel)
		self.assertEqual(response.status_code, 201)

	def test_cancel_parcel(self):
		response = self.client.put('/api/v1/parcels/3/cancel')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Cancelled', str(response.data))


if __name__ == '__main__':
    unittest.main()