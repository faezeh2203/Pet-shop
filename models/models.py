from app import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')  # 'user' or 'admin'
    
    # روابط
    orders = db.relationship('Order', backref='user', lazy=True)
    cart = db.relationship('Cart', backref='user', uselist=False)  # یک سبد خرید به ازای هر کاربر
    
    def __init__(self, username, email, password_hash, role='user'):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
    
    def __repr__(self):
        return f"<User {self.username}>"

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # آدرس تصویر
    
    # روابط
    order_products = db.relationship('OrderProduct', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    
    def __init__(self, name, breed, price, image_url=None):
        self.name = name
        self.breed = breed
        self.price = price
        self.image_url = image_url
    
    def __repr__(self):
        return f"<Product {self.name} ({self.breed})>"

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # روابط
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)
    
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<Cart {self.id} for User {self.user_id}>"

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, cart_id, product_id, quantity):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return f"<CartItem {self.cart_id} - Product {self.product_id}>"

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'completed', 'shipped', etc.
    
    # روابط
    order_products = db.relationship('OrderProduct', backref='order', lazy=True)
    
    def __init__(self, user_id, total_price, status='pending'):
        self.user_id = user_id
        self.total_price = total_price
        self.status = status
    
    def __repr__(self):
        return f"<Order {self.id}, User {self.user_id}, Status {self.status}>"

class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # قیمت محصول در زمان سفارش
    
    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
    
    def __repr__(self):
        return f"<OrderProduct {self.order_id} - {self.product_id}>"


