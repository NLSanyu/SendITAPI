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

        commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            orders INTEGER,
            delivered INTEGER,
            in_transit INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS parcels (
            id SERIAL PRIMARY KEY,
            owner INTEGER NOT NULL,
            description VARCHAR(255) NOT NULL,
            date_created VARCHAR(255) NOT NULL,
            pickup_location VARCHAR(255) NOT NULL,
            present_location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_parcels (
            user_id INTEGER NOT NULL,
            parcel_id INTEGER NOT NULL,
            PRIMARY KEY (user_id , parcel_id),
            FOREIGN KEY (user_id)
                REFERENCES users (id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (parcel_id)
                REFERENCES parcels (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
        )

        try:
            for command in commands:
                self.cur.execute(command)
            self.cur.close()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.connection.close()

    def tearDown(self):
        try:
            self.connection = psycopg2.connect(database="testdb", user = "postgres", password ="memine", host = "127.0.0.1", port = "5432")
            self.cur = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cur.close()
            self.connection.close()

        commands = (
        """DROP TABLE IF EXISTS users;""",
        """DROP TABLE IF EXISTS parcels;""",
        """DROP TABLE IF EXISTS users_parcels;""",
        )

        try:
            for command in commands:
                self.cur.execute(command)
            self.cur.close()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.connection.close()


    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app
        

		