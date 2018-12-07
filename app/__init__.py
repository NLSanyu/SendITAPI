from flask import Flask
from config import Config
from flask_cors import CORS
import flask_jwt_extended
import flasgger
from flask_jwt_extended import JWTManager
from app.models.models import Tables


tables = Tables()
tables.create_tables()

app = Flask(__name__)
tables.create_tables()
app.config.from_object(Config)
flasgger.Swagger(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
CORS(app)

from app.api import users, parcels, admin 




