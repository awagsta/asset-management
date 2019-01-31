import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
from marshmallow import fields
from webargs.flaskparser import use_args, parser, abort
from models.models import *
from auth import repo_url, getUserIdToken, getUserIdOauth, authenticate
from init import db

asset_args = {
    "gitlab_id": fields.Integer(required=True),
    "asset_name": fields.Str(required=True),
    "description": fields.Str(required=True),
    "image_url": fields.Str(required=True),
    "cloud_services": fields.List(fields.Str(), required=True),
    "industries": fields.List(fields.Str(), required=True)
    }

# Asset CRUD Operations
class Asset(Resource):

    @authenticate
    def get(self, id, user_id):
        asset = AssetModel.query.get(id)
        if asset:
            asset_schema = AssetSchema()
            result = asset_schema.dump(asset)
            return jsonify(result.data)

        else:
            abort(404, 'No Asset Found.')

    @authenticate
    @use_args(asset_args)
    def post(self, user_id, args):
        asset_schema = AssetSchema()

        asset = AssetModel(gitlab_id=args['gitlab_id'], 
            asset_name=args['asset_name'], description=args['description'], 
            image_url=args['image_url'], user_id=user_id)
        
     # Create Cloud Service Objects
        for cs in args['cloud_services']:
            db.session.add(CsModel(AssetModel=asset, service_name=cs))

     #Create Industry Objects
        for industry in args['industries']:
            db.session.add(IndustryModel(AssetModel=asset, industry_name=industry))

        db.session.add(asset)
        db.session.commit()
        result = asset_schema.dump(asset)

        return jsonify(result.data)
    
    # eventually modify to do CS updates?
    @authenticate
    @use_args(asset_args)
    def put(self, args, user_id, id):
        asset = AssetModel.query.get(id)
        asset_schema = AssetSchema()

        if not asset:
            abort(404, 'No Asset Found.')
        
        # if not request.json:
        #     abort(400)
        
        # data = request.get_json()
        db.session.delete(asset)
        db.session.commit()
        
        asset = AssetModel(gitlab_id=args['gitlab_id'], asset_id=id ,
            asset_name=args['asset_name'], description=args['description'], 
            image_url=args['image_url'], user_id=user_id)
        
        for cs in args['cloud_services']:
            db.session.add(CsModel(AssetModel = asset, service_name = cs))
        
        for industry in args['industries']:
            db.session.add(IndustryModel(AssetModel = asset, industry_name = industry))

        db.session.add(asset)
        db.session.commit()
        result = asset_schema.dump(asset)

        return jsonify(result.data)

    @authenticate
    def delete(self, id, user_id):
        asset_schema = AssetSchema()
        asset = AssetModel.query.get(id)

        if not asset:
            abort(204, 'No Asset Found')

        db.session.delete(asset)
        db.session.commit()

        result = asset_schema.dump(asset)

        return jsonify(result.data)

# List all assets in the metadata db
class AllAssets(Resource):
    @authenticate
    def get(self, user_id):
        assets = AssetModel.query.all()
        asset_schema = AssetSchema(many=True)
        result = asset_schema.dump(assets)
        return jsonify(result.data)

#TODO ADD OAuth2 Support
# List all assets in metadata db associated with a user
class AssetList(Resource):

    @authenticate
    def get(self, user_id):
        assets = AssetModel.query.filter(current_user_id=user_id)
        asset_schema = AssetSchema(many=True)
        result = asset_schema.dump(assets)
        return jsonify(result.data)

@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)