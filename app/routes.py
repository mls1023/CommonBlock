from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db
from app.forms import ReviewForm, LoginForm, SignupForm, SearchForm
from app.models import User, Apartment, Review

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
        listings = Apartment.query.filter(
            Apartment.rent >= min_rent, Apartment.rent <= max_rent,
            Apartment.num_bedrooms == num_bedrooms).all()
        return redirect(url_for('search_results', apartment_listings=listings))
    return render_template('search.html', form=form)

@app.route('/search_results')
@login_required
def search_results():
    min_rent = request.args.get('min_rent', type=int)
    max_rent = request.args.get('max_rent', type=int)
    num_bedrooms = request.args.get('num_bedrooms', type=int)
    apartment_listings = Apartment.query.filter(Apartment.rent >= min_rent,
    Apartment.rent <= max_rent,Apartment.num_bedrooms == num_bedrooms).all()
    return render_template('search_results.html', listings=apartment_listings)

@app.route('/edit-account')
@login_required
def edit_account():
    return render_template('edit_account.html')

@app.route('/leave_review', methods=['GET', 'POST'])
@login_required
def leave_review():
    form = ReviewForm()
    form.review_type.choices = [('user', 'User'), ('apartment', 'Apartment')]
    if form.validate_on_submit():
        review_type = form.review_type.data
        rating = form.rating.data
        comment = form.comment.data
        if review_type == 'user':
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            if not user:
                flash('User not found')
                return redirect(url_for('leave_review'))
            review = Review(rating=rating, comment=comment, user_id=user.id, author=current_user)
            db.session.add(review)
            db.session.commit()
            flash('Review submitted successfully')
            return redirect(url_for('index'))
        elif review_type == 'apartment':
            address = form.address.data
            apartment = Apartment.query.filter_by(address=address).first()
            if not apartment:
                flash('Apartment not found')
                return redirect(url_for('leave_review'))
            review = Review(rating=rating, comment=comment, apartment_id=apartment.id, author=current_user)
            db.session.add(review)
            db.session.commit()
            flash('Review submitted successfully')
            return redirect(url_for('index'))
    return render_template('leave_review.html', form=form)

@app.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    return render_template('join_group.html')
