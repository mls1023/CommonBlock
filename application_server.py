from flask import Flask, request

CommonBlock = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    return 'Logged in as %s' % username
