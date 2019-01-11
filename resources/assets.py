import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
from models.models import AssetModel
from models.models import CsModel
from models.models import IndustryModel
from database import db
from auth import getUserId
import gitlab

repo_url = 'www.gitlab.com'

class Asset(Resource):
    def get(self, id):
        asset = AssetModel.query.get(id)
        if asset:
            return jsonify({'asset': asset.to_json()})
        else:
            abort(404, message="Asset {} doesn't exist.".format(id))
    
    def post(self):
        if not request.json:
            abort(400, message="Nothing submitted to server.")
        
        data = request.get_json()
        asset = AssetModel(gitlab_id=data['gitlab_id'], 
            asset_name=data['asset_name'], description=data['description'], image_url=data['image_url'])
        
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
            abort(404, message="Asset {} doesn't exist".format(id))
        
        if not request.json:
            abort(400, message="Nothing submitted to server.")
        
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
            abort(404, message="Asset {} doesn't exist.".format(id))
        db.session.delete(id)
        db.session.commit()
        return jsonify({'asset': asset})


class AllAssets(Resource):
    def get(self):
        assets = AssetModel.query.all()
        assetList = []
        for asset in assets:
            assetList.append(asset.to_json())
        return jsonify({'assets': assetList})

class AssetList(Resource):
    def get(self, token):
        user_id = getUserId(token)
        assets = AssetModel.query.filter(current_user_id=user_id)
        json_data = []
        for asset in assets:
            json_data.append(asset.to_json())
        
        return jsonify({"Assets": json_data})
        
