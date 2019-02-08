import sys
import os
sys.path.append('..')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
Create the Flask application.
:return: The application.
"""
def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app