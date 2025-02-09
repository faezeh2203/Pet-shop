from app import db
from sqlalchemy import Integer , String , Float , Boolean , Column
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default='pending')  # 'pending', 'completed', 'shipped', etc.
    
    # روابط
    order_products = db.relationship('OrderProduct', backref='order', lazy=True)
