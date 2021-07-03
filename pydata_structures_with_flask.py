from flask import Flask, request, jsonfly 
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from datetime import datetime
from sqlite3 import Connection as sqlc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sampledb.file'
app.config['SQL_TRACK_MODIFICATIONS'] = 0
