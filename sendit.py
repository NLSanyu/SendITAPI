from app import app
from app.models.models import Tables 
#models import create_users_table, create_parcels_table, create_users_parcels_table

tables = Tables()
tables.create_tables()

if __name__ == '__main__':
	app.run(debug=True)
