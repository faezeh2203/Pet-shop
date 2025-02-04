from app import db
from sqlalchemy import Integer , String , DateTime , Boolean , Column, Float


class Product (db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    breed = Column(String(100), nullable=False)
    image_url = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    