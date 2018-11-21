import os
import psycopg2
from flask import jsonify

class DatabaseConnection():

    def __init__(self):
        self.connection = None
        self.cur = None
    
    def connect(self):
        try:
            if(os.getenv("FLASK_ENV")) == "Production":
                self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            self.connection = psycopg2.connect(database="testdb", user = "postgres", password ="memine", host = "127.0.0.1", port = "5432")
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


   
    def drop_tables(self):
        commands = (
        """
            DROP TABLE IF EXISTS users
        """,
        """
            DROP TABLE IF EXISTS parcels
        """
        )

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


  
    
    
    
        