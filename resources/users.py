import sys
sys.path.append('..')
from flask_restful import Resource
from flask import request, abort, url_for, jsonify
from auth import repo_url
import gitlab

# add user lookup to ensure user does not already exist.

class User(Resource):
    # This route requires administrator privileges
    def post(self):
        if not request.json:
            abort(400, message="Nothing submitted to the server.")

        data = request.get_json()

        user = {
            'email': data['email'],
            'password': data['password'],
            'username': data['username'],
            'name': data['name']
        }

        # Get OAuth2 Token from cookie if it exists.
        oauth_cookie = request.cookies.get('access_token')

        if oauth_cookie:
            oauth_token = cookie
            with gitlab.Gitlab(repo_url, ssl_verify=False, oauth_token=oauth_token) as gl:
                user = gl.users.create(user)
        
        elif data['token']:
            token = data['token']
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                user = gl.users.create(user)
        else:
            abort(401, message="Unauthorized.")
        
        return jsonify({'user': user.attributes, 'id': url_for('get_user', 
        id=user.attributes.id, _external=True)})

    def get(self, id):
        with gitlab.Gitlab(repo_url) as gl:
            user = gl.users.get(id)
        return jsonify({'user': user.attributes})


class UserList(Resource):
    def get(self, token):

        with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
            users = gl.users.list()
            userList = []
            for user in users:
                userList.append({"user": user.attributes})
        return jsonify({'Users': userList})
