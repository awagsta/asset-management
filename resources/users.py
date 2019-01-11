from flask_restful import Resource
from flask import request, abort
import gitlab

class User(Resource):
    def post():
        if not request.json:
            abort(400, message="Nothing submitted to the server.")
        
        data = request.get_json()

        with gitlab.Gitlab(repo_url) as gl:
            gl.users.create({})