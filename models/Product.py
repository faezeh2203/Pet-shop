from app import db
from sqlalchemy import Integer , String , DateTime , Boolean , Column, Float


class Product (db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    image_url = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    
    order_products = db.relationship('OrderProduct', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)