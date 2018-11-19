import psycopg2

class DatabaseTables():

    command = ""

    def __init__(self):
        try:
            self.connection = psycopg2.connect(database="testdb", user = "postgres", password ="memine", host = "127.0.0.1", port = "5432")
            #self.connection.autocommit = True
            self.cur = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_users_table(self):
        command = """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            no_of_orders INTEGER,
            no_delivered INTEGER,
            no_in_transit INTEGER
        )
        """

        try:
            self.cur.execute(command)
            self.cur.close()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.connection.close()

    def create_parcels_table(self):
        command = """
        CREATE TABLE parcels (
            id SERIAL PRIMARY KEY,
            owner VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            date_created VARCHAR(255) NOT NULL,
            pickup_location VARCHAR(255) NOT NULL,
            present_location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            price VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
        """
        try:
            self.cur.execute(command)
            self.cur.close()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.connection.close()

    def create_users_parcels_table(self):
        command = """
        CREATE TABLE user_parcels (
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
        try:
            self.cur.execute(command)
            self.cur.close()
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.connection.close()



  
    
    
    
        