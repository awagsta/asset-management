import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from init import create_app, db
from resources.assets import *
from resources.users import *
from resources.projects import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()
db.create_all(app=app)

api = Api(app)

api.add_resource(Asset, '/asset/<int:id>', endpoint='get_asset')
api.add_resource(Asset, '/asset/')
api.add_resource(AllAssets, '/assets/')
api.add_resource(UserList, '/users/<string:token>')
api.add_resource(User, '/users/<int:id>', endpoint='get_user')
api.add_resource(User, '/users/', '/users/<int:id>/<string:token>')
#api.add_resource(AllProjects, '/allprojects/<string:token>')
api.add_resource(Project, '/project/<int:id>/<string:token>')
api.add_resource(Project_List, '/projects/<string:token>')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    