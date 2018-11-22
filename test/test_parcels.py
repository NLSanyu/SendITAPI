import unittest
import os
import json
import pytest
from test.test_base import BaseTest
from app.models.models import Tables
from app import app

parcel = {"pickup_location": "Plot 1 Kampala Road", "destination": "Plot 5 Jinja Road", "description": "White envelope"}
admin_user = {"username": "admin", "email": "adm@gmail.com", "password": "admin"}
login_user = {"username": "sanyu", "password": "pass123"}
signup_user = {"username": "sanyu", "email": "sanyu@gmail.com", "password": "pass123"}


class APITest(BaseTest):
	def test_home(self):
		"""
			Test for fetching all parcel delivery orders
		"""
		response = self.client.get('/api/v1')
		self.assertEqual(response.status_code, 200)

	def test_create_parcel(self):
		"""
			Test for creating a parcel
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_token()
		response = self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		self.assertEqual(response.status_code, 201)
		self.assertIn("parcel created", str(response.json))


	def test_get_parcels(self):
		"""
			Test for fetching all parcels
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_admin_token()
		self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		response = self.client.get('/api/v1/parcels', content_type='application/json', headers={'Authorization': token})
		self.assertEqual(response.status_code, 200)

	def test_get_one_parcel(self):
		"""
			Test for fetching one parcel
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_token()
		self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		response = self.client.get('/api/v1/parcels/1', content_type='application/json', headers={'Authorization': token})
		self.assertEqual(response.status_code, 200)

	def test_cancel_parcel(self):
		"""
			Test for cancelling a parcel
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_token()
		self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		response = self.client.put('/api/v1/parcels/1/cancel', content_type='application/json', headers={'Authorization': token})
		self.assertEqual(response.status_code, 200)
		self.assertIn("parcel cancelled", str(response.json))

	def test_change_parcel_dest(self):
		"""
			Test for changing a parcel's destination
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_token()
		self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		dest = {"destination": "Kampala"}
		response = self.client.put('/api/v1/parcels/1/destination', json=dest, headers={'Authorization': token})
		self.assertEqual(response.status_code, 200)
		self.assertIn("parcel destination changed", str(response.json))

	def test_change_parcel_status(self):
		"""
			Test for changing a parcel's status
		"""
		self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
		token = self.get_token()
		status = {"status": "Not picked up"}
		self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
		token = self.get_admin_token()
		response = self.client.put('/api/v1/parcels/1/status', json=status, headers={'Authorization': token})
		self.assertEqual(response.status_code, 200)
		self.assertIn("parcel status updated", str(response.json))

	# def test_change_parcel_present_location(self):
	# 	"""
	# 		Test for changing a parcel's present location
	# 	"""
	# 	self.client.post('/api/v1/auth/signup', data=json.dumps(signup_user), content_type='application/json')
	# 	token = self.get_token()
	# 	self.client.post('/api/v1/parcels', data=json.dumps(parcel), content_type='application/json', headers={'Authorization': token})
	# 	location = {"location": "Kampala Road"}
	# 	token = self.get_admin_token()
	# 	response = self.client.put('/api/v1/parcels/1/presentLocation', json=location, headers={'Authorization': token})
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertIn("parcel present location updated", str(response.json))

if __name__ == '__main__':
    unittest.main()
