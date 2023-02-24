from flask import redirect, render_template, url_for, flash, request
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
from app import app, db, login_manager, bcrypt
from app import forms
from app.models import Book, User, ReservationRequest
from app.utils import save_picture
from sqlalchemy.orm import sessionmaker

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


# display the button
@app.route('/book/<int:id>', methods=['GET', 'POST']) 
def book(id):
    book = Book.query.get(id)
    current_user_id = current_user.get_id()  
    is_logged = current_user.is_authenticated
    is_owner = current_user.is_authenticated and int(current_user_id) == int(book.user_id)
    is_in_wishlist = is_owner == False and is_logged == True and book in current_user.wished_books
    return render_template('book_detail.html', book=book, is_owner=is_owner, is_logged=is_logged, is_in_wishlist=is_in_wishlist)


# handle the button click
@app.route('/books/<int:book_id>/wishlist', methods=['GET'])
@login_required
def add_to_wishlist(book_id):
    book = Book.query.get(book_id)
    current_user.wished_books.append(book)
    db.session.add(current_user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/books/<int:book_id>/wishlist/remove', methods=['GET'])
@login_required
def remove_from_wishlist(book_id):
    book = Book.query.get(book_id)
    current_user.wished_books.remove(book)
    db.session.add(current_user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/wishlist', methods=['GET'])
@login_required
def wishlist():
    wished_books = current_user.wished_books
    return render_template('wishlist.html', wished_books=wished_books)


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
      return redirect(url_for("my_offers", form=False, books=books))
    return render_template('my_offers.html',form=forma, books=books)


@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    forma = forms.BookForm()
    book = Book.query.get(id)
    if forma.validate_on_submit() :
        book.title = forma.title.data
        book.author = forma.author.data
        book.year = forma.year.data
        book.summary = forma.summary.data
        db.session.commit()
        return redirect(url_for('my_offers'))
    forma.title.data = book.title
    forma.author.data = book.author
    forma.year.data = book.year
    forma.summary.data = book.summary
    return render_template("update.html", form=forma, book=book)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    offer = Book.query.get(id)
    db.session.delete(offer)
    db.session.commit()
    return redirect(url_for('my_offers'))


@app.route('/books/<int:book_id>/wishlist/order', methods=['GET'])
@login_required
def add_to_order(book_id):
    book = Book.query.get(book_id)
    current_user.ordered_books.append(book)
    flash(f"Book is added to your orders", 'success')
    db.session.add(current_user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/books/<int:book_id>/order/remove', methods=['GET'])
@login_required
def remove_from_orders(book_id):
    book = Book.query.get(book_id)
    current_user.ordered_books.remove(book)
    db.session.add(current_user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/order', methods=['GET'])
@login_required
def order():
    ordered_books = current_user.ordered_books
    user_reservation_requests = User.query.join(ReservationRequest, User.id == ReservationRequest.user_id)\
        .join(Book, ReservationRequest.book_id == Book.id)\
        .filter(Book.user_id == current_user.get_id())\
        .add_columns(Book.title, User.name.label('name'), ReservationRequest.user_id.label('user_id'), ReservationRequest.book_id.label('book_id'))

    return render_template('order.html', ordered_books=ordered_books, user_reservation_requests=user_reservation_requests)


@app.route('/reject-reservation/book/<int:book_id>/user/<int:user_id>', methods=['GET'])
@login_required
def reject_reservation(book_id, user_id):
    reservation = ReservationRequest.query.filter_by(user_id=user_id, book_id=book_id).first()
    if not reservation:
        return "no such reservation"

    book = Book.query.get(book_id)

    if book.user != current_user:
        return "book does not belong to you"
    
    db.session.delete(reservation)
    db.session.commit()
        
    return redirect(request.referrer)


@app.route('/approve-reservation/book/<int:book_id>/user/<int:user_id>', methods=['GET'])
@login_required
def approve_reservation(book_id, user_id):
    reservation = ReservationRequest.query.filter_by(user_id=user_id, book_id=book_id).first()
    if not reservation:
        return "no such reservation"

    book = Book.query.get(book_id)

    if book.user != current_user:
        return "book does not belong to you"
    
    book.assigned_to = user_id
    db.session.delete(reservation)
    db.session.commit()
        
    return redirect(request.referrer)