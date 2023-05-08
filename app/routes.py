from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from pymysql import NULL   
from sqlalchemy import func
from app import app, db
from app.forms import LoginForm, SignupForm, SearchForm, EditAccount, StoreForm, UserReviewForm, ApartmentReviewForm, ChatForm1, ChatForm2
from app.models import User, Apartment, Review, Account, Furniture, Chatrooms, Messages
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
            review = Review(rating=rating,comment=comment,user_id=username)
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
    form = ChatForm1()
    form.chatuser.choices = [(a.username) for a in User.query.all()]
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        chatuser = form.chatuser.data
        num1 = Chatrooms.query.filter_by(user1=chatuser,user2=user.username).count()
        num2 = Chatrooms.query.filter_by(user2=chatuser,user1=user.username).count()
        if num1==0 and num2==0:
            new_room = Chatrooms(user1=chatuser,user2=user.username)
            chatroom_id=new_room.chatroom_id
            db.session.add(new_room)
            db.session.commit()
        else:
            if num1 > 0:
                chatroom = Chatrooms.query.filter_by(user1=chatuser,user2=user.username).first()
                chatroom_id = chatroom.chatroom_id
            if num2 > 0:
                chatroom = Chatrooms.query.filter_by(user2=chatuser,user1=user.username).first()
                chatroom_id = chatroom.chatroom_id
        # cursor = conn.cursor()
        # query = "SELECT chatroom_id FROM chatrooms WHERE (user1=%s AND user2=%s) OR (user1=%s AND user2=%s);"
        # cursor.execute(query,(chatuser,user.username,user.username,chatuser))
        # chatroom = cursor.fetchone()
        # cursor.close()
        #cursor = conn.cursor()
        #query = "SELECT * FROM messages WHERE (chatroom_id=%s);"
        #cursor.execute(query, chatroom_id)
        #data = cursor.fetchall()
        #cursor.close()
        return redirect(url_for('group', chatroom_id=chatroom_id))
    return render_template('join_group.html', form=form)

@app.route('/join_group/group')
@login_required
def group():
    form = ChatForm2()
    chatroom_id = request.args.get('chatroom_id', type=int)
    cursor = conn.cursor()
    query = "SELECT * FROM messages WHERE (chatroom_id=%s);"
    cursor.execute(query, chatroom_id)
    data = cursor.fetchall()
    cursor.close()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        chatext = form.chatext.data
        new_text = Messages(num=NULL, chatroom_id=chatroom_id, user=user.username,text_message=chatext)
        db.sessions.add(new_text)
        db.sessions.commit()
        cursor = conn.cursor()
        query = "INSERT INTO messages(num, chatroom_id,user,text_message) VALUES (NULL,%s,%s,%s)"
        cursor.execute(query)
        conn.commit()
    return render_template('group.html', form=form, messages=data, chatroom_id=chatroom_id)

@app.route('/store', methods=['GET'])
@login_required
def store():
    furniture = Furniture.query.all()
    return render_template('store.html',furniture=furniture )

@app.route('/store/post', methods=['GET', 'POST'])
@login_required
def post_item():
    form = StoreForm()
    if form.validate_on_submit():
        new_item = Furniture(seller_id=current_user.id, condition=form.condition.data,
         price=form.price.data, description=form.description.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Your item has been posted!', 'success')
    return render_template('store_post.html',  form=form)