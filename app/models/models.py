import os
import psycopg2
from flask import jsonify

class DatabaseConnection():
    
    host = 'ec2-54-204-36-249.compute-1.amazonaws.com'
    database = 'deu2c9vgu0pnkt'
    user = 'gxncljkshyqyzc'
    password = '301e6b060431d6daeb1db6a79d01452abb971fc2e21fe62b9afc5ef38f98e9ae'

    def __init__(self):
		host = self.host
		database = self.database
		user = self.user
		password = self.password
		self.connection = None
		self.cur = None
    
    def connect(self):
        try:
            #self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            self.connection = psycopg2.connect(host=str(self.host), database=str(self.database), user=str(self.user), password=str(self.password))
            self.cur = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self.cur.close()
            self.connection.close()

class Tables():

    def create_tables(self):
        commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone_number VARCHAR(255),
            password_hash VARCHAR(255) NOT NULL,
            orders INTEGER,
            delivered INTEGER,
            in_transit INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS parcels (
            id SERIAL PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            description VARCHAR(255) NOT NULL,
            date_created VARCHAR(255) NOT NULL,
            pickup_location VARCHAR(255) NOT NULL,
            present_location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
        """
        )
        self.execute(commands)

   
    def drop_tables(self):
        commands = (
        """
            DROP TABLE IF EXISTS users
        """,
        """
            DROP TABLE IF EXISTS parcels
        """
        )
        self.execute(commands)

    def execute(self, commands):
        try:
            connection = psycopg2.connect(database="testdb", user = "postgres", password ="memine", host = "127.0.0.1", port = "5432")
            cur = connection.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cur.close()
            connection.close()

    
    
        

    
    
        
