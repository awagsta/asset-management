import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
# from webargs import fields
# from webargs.flaskparser import use_args
from models.models import *
from auth import repo_url, getUserIdToken, getUserIdOauth, authenticate
from init import db

# Asset CRUD Operations
class Asset(Resource):

    @authenticate
    def get(self, id, user_id):
        asset = AssetModel.query.get(id)
        asset_schema = AssetSchema()
        result = asset_schema.dump(asset)

        if asset:
            return jsonify(result.data)

        else:
            abort(404, 'No Asset Found.')

    @authenticate
    def post(self, user_id):
        asset_schema = AssetSchema()

        if not request.json:
            abort(400)
        
        data = request.get_json()
        
        asset = AssetModel(gitlab_id=data['gitlab_id'], 
            asset_name=data['asset_name'], description=data['description'], 
            image_url=data['image_url'], user_id=user_id)
        
     # Create Cloud Service Objects
        for cs in data['cloud_services']:
            db.session.add(CsModel(AssetModel=asset, service_name=cs))

     #Create Industry Objects
        for industry in data['industries']:
            db.session.add(IndustryModel(AssetModel=asset, industry_name=industry))

        db.session.add(asset)
        db.session.commit()
        result = asset_schema.dump(asset)

        return jsonify(result.data)
    
    # eventually modify to do CS updates?
    @authenticate
    def put(self, id, user_id):
        asset = AssetModel.query.get(id)
        asset_schema = AssetSchema()

        if not asset:
            abort(404, 'No Asset Found.')
        
        if not request.json:
            abort(400)
        
        data = request.get_json()

        asset.gitlab_id = data['gitlab_id']
        asset.asset_name = data['asset_name']
        asset.description = data['description']
        asset.image_url = data['image_url']

        db.session.commit()
        result = asset_schema.dump(asset)

        return jsonify(result.data)

    @authenticate
    def delete(self, id, user_id):
        asset_schema = AssetSchema()
        asset = AssetModel.query.get(id)

        if not asset:
            abort(204, 'No Asset Found')

        db.session.delete(id)
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
