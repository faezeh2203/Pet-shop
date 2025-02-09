from app import db
from sqlalchemy import Integer , Column, Float

class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
