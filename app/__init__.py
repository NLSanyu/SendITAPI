from flask import Flask
from config import Config
import flask_jwt_extended
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

from app.api import users, parcels, admin
