from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField, TextAreaField, HiddenField, FloatField, FileField, DecimalField
from wtforms.validators import DataRequired, Email, Length, InputRequired, NumberRange

class SearchForm(FlaskForm):
    min_rent = IntegerField('Minimum Rent', validators=[DataRequired()])
    max_rent = IntegerField('Maximum Rent', validators=[DataRequired()])
    num_bedrooms = IntegerField('Number of Bedrooms', validators=[DataRequired()])
    lat = HiddenField(validators=[DataRequired()])
    lng = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Search')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class AccountInfoForm(FlaskForm):
    first_name = StringField('First Name', valaidators=[Length(max=20)])
    last_name = StringField('Last Name', valaidators=[Length(max=20)])
    gender = SelectField('Gender', choices=[('Male'),('Female'),('Other')])
    wake_up = SelectField('Wake Up Time', choices=[('6am'),('7am'),('8am'),('9am'),('10am'),('11am')])
    bedtime = SelectField('Bed Time', choice=[('9pm'),('10pm'),('11pm'),('12am'),('1am'),('2am')])
    edit_account = SubmitField('Edit Account')

class ApartmentReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment')
    apartment_id = SelectField('Apartment', choices=[], coerce=int)

class UserReviewForm(FlaskForm):
    username = TextAreaField('Username', validators=[InputRequired()])
    rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment')


class StoreForm(FlaskForm):
    #name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    condition = SelectField('Condition', choices=[('new', 'New'), ('used', 'Used')], validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    #image = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Post')    