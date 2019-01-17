import sys
sys.path.append('..')
from flask_restful import Resource
from flask import request, abort, url_for, jsonify
from auth import repo_url
import gitlab
from gitlab.exceptions import *

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

 
        if 'token' in data:
            token = data['token']
        else:
            abort(403)

        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                user = gl.users.create(user)

        except GitlabCreateError as error:
            abort(400, 'Bad Request. Could not Create User.')
        except GitlabAuthenticationError as error:
            abort(403, 'User Unauthorized.')
        
        return jsonify({'user': user.attributes, 'id': url_for('get_user', 
        id=user.attributes['id'], _external=True)}), 201

    def get(self, id):
        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False) as gl:
                user = gl.users.get(id)

        except GitlabGetError as error:
            abort(404, 'Gitlab Resource Not Found.')

        return jsonify({'user': user.attributes})
    
    def delete(self, id, token):
        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                gl.users.delete(id)

            return jsonify({'User deleted.'})

        except GitlabDeleteError as error:
            abort(204, 'Resource not found.')
        except GitlabAuthenticationError as error:
            abort(403, 'User Unauthorized.')


class UserList(Resource):
    # Requires API privileges
    def get(self, token):
        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                users = gl.users.list()
                userList = []

                for user in users:
                    userList.append({user.attributes})

        except GitlabAuthenticationError as error:
            abort(403, 'User Unauthorized.')

        return jsonify({'Users': userList})
