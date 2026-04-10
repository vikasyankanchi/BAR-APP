from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'owner' or 'staff'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category_order = db.Column(db.Integer, default=99)
    products = db.relationship('Product', backref='category', lazy=True)

class MLSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=True, nullable=False)
    products = db.relationship('Product', backref='ml_size', lazy=True)

class CategoryMLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    ml_id = db.Column(db.Integer, db.ForeignKey('ml_size.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    ml_id = db.Column(db.Integer, db.ForeignKey('ml_size.id'), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    stock_entries = db.relationship('StockEntry', backref='product', lazy=True)

class StockEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    opening_stock = db.Column(db.Integer, nullable=False)
    new_stock = db.Column(db.Integer, default=0)
    total_available_stock = db.Column(db.Integer, default=0)
    closing_stock = db.Column(db.Integer, default=0)
    sold = db.Column(db.Integer, default=0)
    cost_price_at_entry = db.Column(db.Float, nullable=False)
    selling_price_at_entry = db.Column(db.Float, nullable=False)
    
    # STATUS FIELDS
    is_completed = db.Column(db.Boolean, default=False)
    entry_type = db.Column(db.String(20), default='Pending') # Pending, Regular, Closed, Estimated

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(250))
