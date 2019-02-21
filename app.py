import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from webargs.flaskparser import parser, abort
from init import create_app, db
from resources.assets import *
from resources.users import *
from resources.projects import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()
db.create_all(app=app)

api = Api(app)

api.add_resource(AssetDetails, '/asset/details/<int:id>')
api.add_resource(Asset, '/asset/')
api.add_resource(Asset, '/asset/<int:id>', endpoint='get_asset')
api.add_resource(AllAssets, '/assets/')
api.add_resource(AssetList, '/assets/list/')
api.add_resource(UserList, '/users/')
api.add_resource(User, '/users/<int:id>', endpoint='get_user')
api.add_resource(User, '/users/')
#api.add_resource(AllProjects, '/allprojects/<string:token>')
api.add_resource(Project, '/project/<int:id>/')
api.add_resource(Project_List, '/projects/')

@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    