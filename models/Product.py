from app import db
from sqlalchemy import Integer , String , DateTime , Boolean , Column


class Product (db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    breed = db.Column(String(100), nullable=False)
    image_url = db.Column(String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    