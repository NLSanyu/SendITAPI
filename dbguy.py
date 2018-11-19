import psycopg2

try:
    connection = psycopg2.connect(database="testdb", user = "postgres", password ="memine", host = "localhost", port = "5432")
    cur = connection.cursor()
    print("Success")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)

query = """SELECT * FROM parcels;"""
#cur.execute(query)
cur.execute(query)
res = cur.fetchall()
for row in res:
    print(row[1])


query = """ INSERT INTO users (username, email, passwor) VALUES ('lydia', 'lydia@gmail.com', 'pass123')"""
print(cur.execute(query))
