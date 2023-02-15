from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms.validators import DataRequired, ValidationError, EqualTo
import app

class RegisterForm(FlaskForm):
    name = StringField('Full Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeat_password = PasswordField("Repeat Password", [EqualTo('password', "Password have to macth.")])
    submit = SubmitField('Register')

    def check_name(self, name):
        user = app.User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This name is used. Please enter other name.')

    def check_email(self, email):
        user = app.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is used. Please enter other email.')
            
class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class BookForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=25)])
    author = StringField('Author', [DataRequired(), Length(max=25)])
    year = FloatField('Year', [DataRequired()])
    summary = TextAreaField('Summary', [DataRequired(), Length(max=3500)])
    photo = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
 