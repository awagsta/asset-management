import sys
sys.path.append('..')
from flask import url_for
from marshmallow import Schema, fields
from init import db

class AssetModel(db.Model):
    __tablename__ = 'assets'
    user_id = db.Column(db.Integer, nullable=False)
    asset_id = db.Column(db.Integer, primary_key=True)
    gitlab_id = db.Column(db.Integer, nullable=False)
    asset_name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    cloud_services = db.relationship('CsModel', backref='AssetModel')
    industries = db.relationship('IndustryModel',  backref='AssetModel')    

class CsModel(db.Model):
    __tablename__: 'cloud_services'
    cs_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id'))

class IndustryModel(db.Model):
    __tablename__: 'industries'
    industry_id = db.Column(db.Integer, primary_key=True)
    industry_name = db.Column(db.String(100))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id'))

class IndustrySchema(Schema):
    class Meta:
        strict = True

    industry_name = fields.Str(required=True)

class CsSchema(Schema):
    class Meta:
        strict = True
    service_name = fields.Str(required=True)

class AssetSchema(Schema):
    class Meta:
        strict = True

    user_id = fields.Integer(dump_only=True)
    asset_id = fields.Integer(dump_only=True)
    gitlab_id = fields.Integer(required=True)
    asset_name = fields.Str(required=True)
    description = fields.Str(required=True)
    image_url = fields.Str(required=True) # replace with fields.url
    industries = fields.Nested(IndustrySchema, many=True)
    cloud_services = fields.Nested(CsSchema, many=True)