import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://doadmin:AVNS_LBcEvyS29yQsLJaEDU9@db-mysql-fra1-18058-do-user-13718757-0.b.db.ondigitalocean.com:25060/defaultdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register'
login_manager.login_message_category = 'info'



from app import views
from app.models import Book, User


