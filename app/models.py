from app import db, login_manager, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Common-Block")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

membership = db.Table('membership',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
    groups = db.relationship('Group', secondary=membership, back_populates='members', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Furniture(db.Model):
    __tablename__ = 'furniture'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref='furniture', lazy=True)
    #^fix the above database, i think im using bakref and backpopulates incorrectly but it should work similar to reviews
    #uncommenting the user line breaks the database structure so for now I wouldnt 

    def save_image(self, image):
        print('hi')
        #edit this function to save an image

    def __repr__(self):
        return f"Furniture('{self.name}', '{self.condition}', '{self.price}')"

class Apartment(db.Model):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    rent = db.Column(db.Integer, nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False)
    lat = db.Column(db.DECIMAL(7, 4), nullable=False)
    lng = db.Column(db.DECIMAL(7, 4), nullable=False)

    def __repr__(self):
        return '<Apartment Listing {}>'.format(self.address)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', backref='reviews')
    apartment = db.relationship('Apartment', backref='reviews')



class Account(db.Model):
    __tablename__='account'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)

class Chatrooms(db.Model):
    __tablename__='chatrooms'
    chatroom_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user1 = db.Column(db.String(20), nullable=False)
    user2 = db.Column(db.String(20), nullable=False)


class Messages(db.Model):
    __tablesname__='messages'
    num = db.Column(db.Integer, primary_key=True, nullable=False)
    chatroom_id = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(20), nullable=False)
    text_message = db.Column(db.String(150),nullable=False)



class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    members = db.relationship('User', secondary=membership, back_populates='groups', lazy=True)

    def __repr__(self):
        return '<Group {}>'.format(self.name)
