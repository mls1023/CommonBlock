from flask import Flask, render_template, request, redirect, url_for

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission here
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/edit-account')
def edit_account():
    return render_template('edit_account.html')

@app.route('/leave-review')
def leave_review():
    return render_template('leave_review.html')

@app.route('/join-group')
def join_group():
    return render_template('join_group.html')

if __name__ == '__main__':
    app.run(debug=True)
