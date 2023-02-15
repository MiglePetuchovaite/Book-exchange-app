import os
from flask import Flask, redirect, render_template, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
import secrets
from PIL import Image
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.app_context().push()
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'books.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register'
login_manager.login_message_category = 'info'

class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column("Full Name", db.String(20), unique=True, nullable=False)
  email = db.Column("Email", db.String(120), unique=True, nullable=False)
  password = db.Column("Password", db.String(60), unique=True, nullable=False)


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


@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    return User.query.get(int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        coded_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=coded_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful! Log in!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Failed to sign in. Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile")
@login_required
def account():
    return render_template('profile.html')


@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/book/<int:id>')
def book(id):
    book = Book.query.get(id)
    return render_template('book_detail.html', book=book)


@app.route('/my_wishes')
def wishlist():
    return render_template('my_wishes.html')


@app.route('/my_offers', methods=['GET', 'POST'])
@login_required
def my_offers():
    books = Book.query.filter_by(user_id=current_user.id).all()
    forma = forms.BookForm()
    if forma.validate_on_submit():
      if forma.photo.data:
          photo_path = save_picture(forma.photo.data)

      new_offer = Book(title=forma.title.data, author=forma.author.data, year=forma.year.data, summary=forma.summary.data, photo=photo_path, user_id=current_user.id)

      db.session.add(new_offer)
      db.session.commit()
      books = Book.query.filter_by(user_id=current_user.id).all()
      flash(f"Book is added", 'success')
      return redirect(url_for("index", form=False, books=books))
    return render_template('my_offers.html',form=forma, books=books)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    picture_relative_path = '/static/images/' + picture_fn

    output_size = (225, 225)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_relative_path

# @app.route("/")
# def index():
#     return render_template("index.html")


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

