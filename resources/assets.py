import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
from marshmallow import fields
from webargs.flaskparser import use_args
from models.models import *
from auth import repo_url, getUserIdToken, getUserIdOauth, authenticate
from init import db

#webargs expected fields in post body for asset submission
asset_args = {
    "gitlab_id": fields.Integer(required=True),
    "asset_name": fields.Str(required=True),
    "description": fields.Str(required=True),
    "image_url": fields.Str(required=True),
    "cloud_services": fields.List(fields.Str(), required=True),
    "industries": fields.List(fields.Str(), required=True),
    "Private-Token": fields.Str(required=True)
    }

# Asset CRUD Operations
class Asset(Resource):
    """
    Asset represents an API resource for a single asset
    and it's associated CRUD operations.
    """

    @authenticate
    def get(self, id, user_id):
        """
        Get an asset from the metadata database.
        :param id: The id of the asset to retrieve
        :return: The Asset.
        """

        asset = AssetModel.query.get(id)
        if asset:
            asset_schema = AssetSchema()
            result = asset_schema.dump(asset)
            return jsonify(result.data)

        else:
            abort(404, 'No Asset Found.')

    @use_args(asset_args, locations=("json", "headers"))
    def post(self, args):
        """
        Post an asset to the metadata database.
        :param args: The asset args retrieved from the POST body
        :param user_id: retrieved from the authenticate function
        :return: the inserted asset.
        """

        
        asset_schema = AssetSchema()
        user_id = getUserIdToken(args['Private-Token'])

        asset = AssetModel(gitlab_id=args['gitlab_id'], 
            asset_name=args['asset_name'], description=args['description'], 
            image_url=args['image_url'], user_id=user_id)
        
        print(args['cloud_services'])

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
    

    @use_args(asset_args, locations=("json", "headers"))
    def put(self, args, id):
        """
        Update an asset in the metadata database.
        :param args: the asset args retrieved from the POST body
        :param id: the id of the asset to update
        :param user_id: retrieved from the authentication function
        :return: the updated asset if found.
        """

        asset = AssetModel.query.get(id)
        asset_schema = AssetSchema()
        user_id = getUserIdToken(args['Private-Token'])

        if not asset:
            abort(404, 'No Asset Found.')
        
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
        """
        Delete an asset from the metadata database.
        :param id: the id of the asset to remove
        :param user_id: retrieved from the authentication function
        :return: the deleted asset if found.
        """
        
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
    """
    AllAssets represents an API resource for a list of all the assets.
    """
    @authenticate
    def get(self, user_id):
        """
        Get a list of all assets from the metadata database.
        :param user_id: retrieved from the authentication function
        :return: all assets from the metadata database.
        """
        assets = AssetModel.query.all()
        asset_schema = AssetSchema(many=True)
        result = asset_schema.dump(assets)
        return jsonify(result.data)

#TODO ADD OAuth2 Support
# List all assets in metadata db associated with the current user
class AssetList(Resource):
    """
    AssetList represents an API resource for a list of assets for a user.
    """
    @authenticate
    def get(self, user_id):
        """
        Get a list of all of the current user's assets from 
        the metadata database.
        :param user_id: retrieved from the authentication function
        :return: list of the current user's assets from the metadata database.
        """
        assets = AssetModel.query.filter_by(user_id=user_id).all()
        asset_schema = AssetSchema(many=True)
        result = asset_schema.dump(assets)
        return jsonify(result.data)


# Get Asset and associated Gitlab project info by asset id
class AssetDetails(Resource):
    """
    AssetDetails represents an API resource for an asset and it's
    associated metadata from gitlab.
    """
    def get(self, id):
        """
        Get an asset and it's associated metadata from the metadata
        database and gitlab.
        :param id: the id of the asset to retrieve
        :return: The Asset and it's gitlab metadata if found.
        """
        asset = AssetModel.query.get(id)

        if not asset:
            abort(404, "No Asset Found.")

        token = request.headers['Private-Token']

        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                project = gl.projects.get(asset.gitlab_id)

        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')
        
        asset_schema = AssetSchema()
        result = asset_schema.dump(asset)
        return jsonify([result.data, project.attributes])