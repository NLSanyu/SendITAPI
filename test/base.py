import unittest
import os
import unittest
from app import app

class BaseTestCase(unittest.TestCase):
    """
        A base test case
    """

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app
