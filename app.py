import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from database import db
from resources.asset import Asset, AssetList

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

api.add_resource(Asset, '/asset/<int:id>', endpoint='get_asset')
api.add_resource(Asset, '/asset/')
api.add_resource(AssetList, '/assets/')
app.run(port=5000, debug=True)