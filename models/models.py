import sys
sys.path.append('..')
from database import db

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