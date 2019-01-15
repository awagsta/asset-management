import sys
sys.path.append('..')
from flask_restful import Resource
from flask import request, abort, url_for, jsonify
from auth import repo_url
import gitlab

# add user lookup to ensure user does not already exist.

class User(Resource):
    # This route requires API privileges
    def post(self):
        if not request.json:
            abort(400)

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
        
        # If no OAuth 2 Token, but private token was provided.
        elif data['token']:
            token = data['token']
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                user = gl.users.create(user)
        else:
            abort(403)
        
        return jsonify({'user': user.attributes, 'id': url_for('get_user', 
        id=user.attributes.id, _external=True)})

    def get(self, id):
        with gitlab.Gitlab(repo_url, ssl_verify=False) as gl:
            user = gl.users.get(id)
        return jsonify({'user': user.attributes})
    
    def delete(self, id, token):
        if token:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                gl.users.delete(id)
                message = {'User with id {} deleted.'.format(id)}
            return jsonify(message)
        else:
            abort(403)


class UserList(Resource):
    # Requires API privileges
    def get(self, token):
        with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
            users = gl.users.list()
            userList = []
            for user in users:
                userList.append({"user": user.attributes})
        return jsonify({'Users': userList})
