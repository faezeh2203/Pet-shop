from app import db
from sqlalchemy import Integer, String, Float, Boolean, Column, DateTime, ForeignKey
from datetime import datetime

class Cart(db.Model):
     id = Column(Integer, primary_key=True)
     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
     product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
     quantity = Column(Integer, nullable=False, default=1)
     created_at = Column(DateTime(), default=datetime.utcnow)
