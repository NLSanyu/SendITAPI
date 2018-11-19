from app import app
from app.models import models 
#models import create_users_table, create_parcels_table, create_users_parcels_table

db = models.Database()
db.create_users_table()
db.create_parcels_table()
db.create_users_parcels_table()

if __name__ == '__main__':
	app.run(debug=True)
