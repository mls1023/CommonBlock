from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import func
from app import app, db
from app.forms import ReviewForm, LoginForm, SignupForm, SearchForm, EditAccount
from app.models import User, Apartment, Review, Account
from geopy.distance import geodesic

import pymysql.cursors
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       db='CommonBlock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Sorry, that username is already taken. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        new_account = Account(user_id=new_user.id, id=new_user.id)
        db.session.add(new_account)
        db.session.commit()
        flash('Congratulations, you have successfully signed up!', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        min_rent = form.min_rent.data
        max_rent = form.max_rent.data
        num_bedrooms = form.num_bedrooms.data
        lat = form.lat.data
        lng = form.lng.data
        return redirect(url_for('search_results', min_rent=min_rent, max_rent=max_rent, num_bedrooms=num_bedrooms, lat=lat, lng=lng))
    return render_template('search.html', form=form)

@app.route('/search_results')
@login_required
def search_results():
    min_rent = request.args.get('min_rent', type=int)
    max_rent = request.args.get('max_rent', type=int)
    num_bedrooms = request.args.get('num_bedrooms', type=int)
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)

    listings = Apartment.query.filter(
    Apartment.rent >= min_rent,
    Apartment.rent <= max_rent,
    Apartment.num_bedrooms == num_bedrooms
    ).all()

    filtered_listings = [listing for listing in listings if
        geodesic((lat,lng), (listing.lat, listing.lng)).miles <= 1]

    reviews = []
    for listing in filtered_listings:
        avg_rating = db.session.query(func.avg(Review.rating)).filter_by(apartment_id=listing.id).scalar()
        rand_reviews = Review.query.filter_by(apartment_id=listing.id).order_by(func.random()).limit(5).all()
        reviews.append({'listing': listing, 'avg_rating': avg_rating, 'rand_reviews': rand_reviews})
    return render_template('search_results.html', reviews=reviews)

@app.route('/edit-account', methods=['GET','POST'])
@login_required
def edit_account():
    form = EditAccount()
    if form.validate_on_submit():
        new_info = Account(id=current_user.id, user_id=current_user.id, first_name=form.first_name.data, last_name=form.last_name.data,age= form.age.data)
        current_account = Account.query.get(current_user.id)
        db.session.delete(current_account)
        db.session.add(new_info)
        db.session.commit()
    return render_template('edit_account.html',form=form)

@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    review_type = None
    search_result = None

    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            text=form.text.data,
            user_id=current_user.id,
            apartment_id=form.apartment_id.data,
        )
        db.session.add(review)
        db.session.commit()
        flash('Review has been submitted successfully.', 'success')
        return redirect(url_for('home'))

    if request.method == 'POST':
        review_type = request.form.get('review_type')
        query = request.form.get('query').strip()
        
        if review_type == 'user':
            search_result = User.query.filter_by(username=query).first()
        elif review_type == 'apartment':
            search_result = Apartment.query.filter_by(address=query).first()
            
        if not search_result:
            flash('No {} found with the given name/address.'.format(review_type), 'danger')
        else:
            form.apartment_id.choices = [(search_result.id, search_result.address)]
            
    return render_template('review.html', form=form, review_type=review_type, search_result=search_result)


@app.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    return render_template('join_group.html')
