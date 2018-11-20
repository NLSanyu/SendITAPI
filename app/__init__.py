from flask import Flask
from config import Config
import flask-jwt-extended
from flask-jwt-extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
from app.api import users, parcels, admin
