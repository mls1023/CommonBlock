from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user   
from sqlalchemy import func
from app import app, db
from app.forms import ApartmentReviewForm, UserReviewForm, LoginForm, SignupForm, SearchForm, StoreForm
from app.models import Furniture, User, Apartment, Review
from geopy.distance import geodesic

import pymysql.cursors
conn = pymysql.connect(host='127.0.0.1',
                       port=8889,
                       user='root',
                       password='root',
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
    listings = Apartment.query.filter(Apartment.rent >= min_rent, Apartment.rent <= max_rent,
    Apartment.num_bedrooms == num_bedrooms).all()
    filtered_listings = [listing for listing in listings if
        geodesic((lat,lng), (listing.lat, listing.lng)).miles <= 1]
    reviews = []
    for listing in filtered_listings:
        avg_rating = db.session.query(func.avg(Review.rating)).filter_by(apartment_id=listing.id).scalar()
        rand_reviews = Review.query.filter_by(apartment_id=listing.id).order_by(func.random()).limit(5).all()
        reviews.append({'listing': listing, 'avg_rating': avg_rating, 'rand_reviews': rand_reviews})
    return render_template('search_results.html', reviews=reviews)

@app.route('/edit-account')
@login_required
def edit_account():
    return render_template('edit_account.html')

@app.route('/review/user', methods=['GET', 'POST'])
@login_required
def user_review():
    form = UserReviewForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        rating = form.rating.data
        comment = form.comment.data
        user = User.query.filter_by(username=username).first()
        if user:
            review = Review(rating=rating,text=comment,user_id=user.id)
            db.session.add(review)
            db.session.commit()
            flash('Review has been submitted successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('User with the given username does not exist.', 'danger')
    return render_template('user_review.html', form=form)
    
@app.route('/review/apartment', methods=['GET', 'POST'])
def apartment_review():
    form = ApartmentReviewForm()
    form.apartment_id.choices = [(a.id, a.address) for a in Apartment.query.all()]
    if form.validate_on_submit():
        review = Review(rating=form.rating.data, comment=form.comment.data)
        apartment = Apartment.query.get(form.apartment_id.data)
        apartment.reviews.append(review)
        db.session.add(apartment)
        db.session.commit()
        flash('Thank you for your review!')
        return redirect(url_for('index'))
    else:
        flash('Incorrect input.', 'danger')
    return render_template('apartment_review.html', form=form)

@app.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    return render_template('join_group.html')

@app.route('/store', methods=['GET'])
def store():
    # Handle GET request to display items and search form
    cursor = conn.cursor()
    getall = 'SELECT * FROM furnitures'
    cursor.execute(getall)
    data = cursor.fetchall()
    cursor.close()
    return render_template('store.html', result = data)

@app.route('/store/post', methods=['GET', 'POST'])
@login_required
def post_item():
    # Handle GET and POST request to post a new item
    form = StoreForm()
    if form.validate_on_submit():
        # picture_file = 0 #edit
        # new_item = Furniture(picture=picture_file, condition=form.condition.data, description=form.description.data, price=form.price.data, seller=current_user)
        
        new_item = Furniture(username=form.username.data, email=form.email.data, item_condition=form.condition.data, price=form.price.data, furniture_name=form.furniture_name.data, description=form.description.data)
        
        db.session.add(new_item)
        db.session.commit()
        flash('Your item has been posted!', 'success')
    return render_template('store_post.html',  form=form)


    # #grabs information from the forms
    # furnitureName = request.form['fname']
    # Condition = request.form['condition']
    # Description = request.form['description']
    # Price = request.form['price']
    # Username = request.form['username']
    # Email = request.form['email']
    # #cursor used to send queries and get item_id
    # cursor = conn.cursor()
    # getAll = 'SELECT * FROM furnitures'
    # cursor.execute(getAll)
    # data = cursor.fetchall()
    # item_id = cursor.rowcount
    # ins = 'INSERT INTO furnitures VALUES(%d, %s, %s, %s, %s, %s, %s)'
    # cursor.execute(ins, (item_id, Username, Email, Condition, Price, furnitureName, Description))
    # conn.commit()
    # cursor.close()

    #return render_template('store_post.html', methods=['GET', 'POST'])

# @app.route('/itemAuth', methods=['GET', 'POST'])
# @login_required
# def itemAuth():
#      #grabs information from the forms
#     furnitureName = request.form['fname']
#     Condition = request.form['condition']
#     Description = request.form['description']
#     Price = request.form['price']
#     Username = request.form['username']
#     Email = request.form['email']
#     #cursor used to send queries and get item_id
#     cursor = conn.cursor()
#     getAll = 'SELECT * FROM furnitures'
#     cursor.execute(getAll)
#     data = cursor.fetchall()
#     #item_id = cursor.rowcount
#     ins = 'INSERT INTO furnitures VALUES(%d, %s, %s, %s, %s, %s, %s)'
#     cursor.execute(ins, (4, Username, Email, Condition, Price, furnitureName, Description))
#     conn.commit()
#     cursor.close()
#     return render_template('store.html', methods=['GET', 'POST'])
