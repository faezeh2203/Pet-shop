from app import db
from models import User
from sqlalchemy import Integer, String, Float, Boolean, Column, DateTime, ForeignKey
from datetime import datetime

class Carts(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)
