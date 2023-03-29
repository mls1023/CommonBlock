from flask import Flask

app = Flask(__name__)

# import any necessary dependencies here, e.g. database connection

from app import routes


