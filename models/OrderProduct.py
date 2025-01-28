from app import db
from sqlalchemy import Integer , Column

class OrderProduct(db.Model):
    order_id = db.Column(Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(Integer, db.ForeignKey('product.id'), primary_key=True)
