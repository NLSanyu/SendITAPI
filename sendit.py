from app import app
from app.models.models import Tables 

tables = Tables()
tables.create_tables()

if __name__ == '__main__':
	app.run(debug=True)
