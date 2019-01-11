import sys
sys.path.append('..')
from flask_restful import Resource
from flask import request, abort
from auth import repo_url
import gitlab

# add user lookup to ensure user does not already exist.
class User(Resource):
    def post(self):
        if not request.json:
            abort(400, message="Nothing submitted to the server.")
        
        data = request.get_json()

        with gitlab.Gitlab(repo_url) as gl:
            user = gl.users.create({data['email'], data['password'], data['user name'], data['name'] })
        
        return jsonify({'username': user.attributes.username, 'id': user.attributes.id})

    def get(self, id):
        with gitlab.Gitlab(repo_url) as gl:
            user = gl.users.get(id)
        return jsonify({'user': user.attributes})
