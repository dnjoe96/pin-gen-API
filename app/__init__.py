from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os
import logging
from flask_pymongo import PyMongo
import africastalking

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mongo = PyMongo(app)


# initializing SDK
# username gotten from Africastalking dashboard
# api_key was generated from the dashboard > settings
# username = 'codeplateu'
# api_key = 'dbc733441e6d1f39d5e028cb976f15c9e0143e3ff93d157d1f4223207e1da63a'

username = 'sandbox'
api_key = 'b936cefee34846ad14bfa102255818e9cab6bfaeb34d4e0f75aeed6646314da2'

africastalking.initialize(username, api_key)
ussd = africastalking.USSD
sms = africastalking.SMS


from app import route, models, card_activation
