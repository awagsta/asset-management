import os
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class AssetModel(db.Model):
    __tablename__ = 'assets'
    asset_id = db.Column(db.Integer, primary_key=True)
    gitlab_id = db.Column(db.Integer, nullable=False)
    asset_name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    cloud_services = db.relationship('CsModel', backref='AssetModel')
    industries = db.relationship('IndustryModel',  backref='AssetModel')

    def to_json(self):
        industryList = []
        for industry in self.industries:
            industryList.append(industry.to_json())
        
        csList = []
        for cs in self.cloud_services:
            csList.append(cs.to_json())

        asset = {
            "gitlab_id": self.gitlab_id,
            "asset_name": self.asset_name,
            "description": self.description,
            "image_url": self.image_url,
            "industries": industryList,
            "cloud_services": csList
        }
        return asset

class CsModel(db.Model):
    __tablename__: 'cloud_services'
    cs_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id'))

    def to_json(self):
        cloud_service = {"cloud_service": self.service_name}
        return cloud_service

class IndustryModel(db.Model):
    __tablename__: 'industries'
    industry_id = db.Column(db.Integer, primary_key=True)
    industry_name = db.Column(db.String(100))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id'))

    def to_json(self):
        industry = {"industry": self.industry_name}
        return industry

@app.route('/assets', methods=['GET'])
def getAssets():
    assets = AssetModel.query.all()
    assetList = []
    for asset in assets:
        assetList.append(asset.to_json())
    return jsonify({'assets': assetList})

@app.route('/asset/<int:id>/', methods=['GET'])
def getAsset():
    asset = AssetModel.query.get(id)
    if asset:
        return jsonify({'asset': asset.to_json()})
    else:
        abort(404, message="Asset {} doesn't exist.".format(id))

@app.route('/asset', methods=['POST'])
def createAsset():
    if not request.json:
        abort(400, "Nothing submitted to the server")
    
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

@app.route('/asset/<int:id>/', methods=['PUT'])
def updateAsset():
    asset = AssetModel.query.get(id)
    if not asset:
        abort(404, message="Asset {} doesn't exist.".format(id))
    
    if not request.json:
        abort(400, "Nothing submitted to server")
    
    data = request.get_json()
    asset.gitlab_id = data['gitlab_id']
    asset.asset_name = data['asset_name']
    asset.description = data['description']
    asset.image_url = data['image_url']
    db.session.commit()
    return jsonify({'asset': asset})

@app.route('/asset/<int:id>/', methods=['DELETE'])
def deleteAsset():
    asset = AssetModel.query.get(id)
    if not asset:
        abort(404, message="Asset {} doesn't exist.".format(id))
    db.session.delete(id)
    db.session.commit()
    return jsonify({'Result': True})

if __name__ == '__main__':
    app.run(debug = True)