from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username_input']
        email = request.form['email_input']
        password = request.form['password_input']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
        login_user(user)
        flash(f'Hello {user.username}, you have been logged in', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/edit-account')
@login_required
def edit_account():
    return render_template('edit_account.html')

@app.route('/leave-review')
@login_required
def leave_review():
    return render_template('leave_review.html')

@app.route('/join-group')
@login_required
def join_group():
    return render_template('join_group.html')
