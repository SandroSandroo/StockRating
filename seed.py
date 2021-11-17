from app import app
from models import db, connect_db

""" create DB tables """

db.drop_all()
db.create_all()