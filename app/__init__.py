from flask import Flask
from config import Config
import flask_jwt_extended
import flasgger
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
flasgger.Swagger(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

from app.api import users, parcels, admin
