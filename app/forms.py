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

class EditAccount(FlaskForm):
    first_name = StringField('First Name', validators=[Length(max=20)])
    last_name = StringField('Last Name',validators=[Length(max=20)])
    age = IntegerField("Age",validators=[InputRequired()])
    submit = SubmitField('Edit Account')

class ChatForm1(FlaskForm):
    chatuser = SelectField('Users', choices=[], validators=[DataRequired()])
class ChatForm2(FlaskForm):
    chatext = TextAreaField("Text",validators=[InputRequired()])

class ApartmentReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment')
    apartment_id = SelectField('Apartment', choices=[], coerce=int)

class UserReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[InputRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment')
    username = TextAreaField('Username', validators=[InputRequired()])

class StoreForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=100)])
    condition = SelectField('Condition', choices=[('new', 'New'), ('like new', 'Like new'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])