from app import db
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey


user_wishlist = Table(
    "user_wishlist",
    db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
)

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", lazy=True)
    users = db.relationship("User", secondary=user_wishlist, back_populates="wished_books")

class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column("Full Name", db.String(20), unique=True, nullable=False)
  email = db.Column("Email", db.String(120), unique=True, nullable=False)
  password = db.Column("Password", db.String(60), unique=True, nullable=False)
  wished_books = db.relationship("Book", secondary=user_wishlist, back_populates="users")