import psycopg2
import unittest
import os
from app import app
from app.models.models import DatabaseConnection

class BaseTestCase(unittest.TestCase):
    """
        A base test case
    """

    def setUp(self):
        try:
            self.connection = psycopg2.connect(database="testdb", user = "postgres", password ="memine", host = "127.0.0.1", port = "5432")
            self.cur = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cur.close()
            self.connection.close()

        

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app
        

		