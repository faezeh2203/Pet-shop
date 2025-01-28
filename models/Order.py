from app import db
from sqlalchemy import Integer , String , Float , Boolean , Column
from datetime import datetime

class Order(db.Model):
    id = db.Column(Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(100),default="Processing")
    user_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    products = db.relationship('Product', secondary='order_product', backref='orders')
