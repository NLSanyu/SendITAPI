from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
#from app import users, parcels
#from app import api
#import api
from app.api import users, parcels

