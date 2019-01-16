import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
from models.models import *
from auth import repo_url, getUserIdToken
from database import db
import gitlab
from gitlab.exceptions import GitlabAuthorizationException

# Asset CRUD Operations
class Asset(Resource):
    def get(self, id):
        asset = AssetModel.query.get(id)
        if asset:
            return jsonify({'asset': asset.to_json()})
        else:
            abort(404, 'No Asset Found.')
    
    def post(self):
        if not request.json:
            abort(400)
        
        data = request.get_json()

        if data['token']:
            try:
                user_id = getUserIdToken(data['token'])
                
            except GitlabAuthorizationException as error:
                abort(403, 'User Unauthorized.')
        else:
            abort(403, 'User Unauthorized.')
        
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

        return jsonify({'Asset': asset.to_json()})
    
    # eventually modify to do CS updates?
    def put(self, id):
        asset = AssetModel.query.get(id)

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

        return jsonify({'asset': asset})

    def delete(self, id):
        asset = AssetModel.query.get(id)

        if not asset:
            abort(204, 'No Asset Found')

        db.session.delete(id)
        db.session.commit()

        return jsonify({'asset': asset})

# List all assets in the metadata db
class AllAssets(Resource):
    def get(self):
        assets = AssetModel.query.all()
        assetList = []

        for asset in assets:
            assetList.append(asset.to_json())

        return jsonify({'assets': assetList})

#TODO ADD OAuth2 Support
# List all assets in metadata db associated with a user
class AssetList(Resource):
    def get(self, token):
        try:
            user_id = getUserIdToken(token)
            assets = AssetModel.query.filter(current_user_id=user_id)
            json_data = []

            for asset in assets:
                json_data.append(asset.to_json())

        except GitlabAuthorizationException as error:
            abort(403, "User Unauthorized.")

        return jsonify({"Assets": json_data})
        
