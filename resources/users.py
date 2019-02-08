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
    """
    User represents an API resource for a user on gitlab.
    """
    def post(self):
        """
        Create a gitlab user through the API. Requires admin privileges.
        :return: The created user.
        """
        if not request.json:
            abort(400)

        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        data = request.get_json()

        user = {
            'email': data['email'],
            'password': data['password'],
            'username': data['username'],
            'name': data['name']
        }


        token = request.headers['Private-Token']

        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                user = gl.users.create(user)

        except GitlabCreateError as error:
            abort(400, 'Bad Request. Could not Create User.')
        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')
        
        return jsonify({'user': user.attributes, 'id': url_for('get_user', 
        id=user.attributes['id'], _external=True)}), 201

    def get(self, id):
        """
        Get a gitlab user by their gitlab user id.
        :param id: the id of the gitlab user
        :return: The user if found.
        """
        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False) as gl:
                user = gl.users.get(id)

        except GitlabGetError as error:
            abort(404, 'Gitlab Resource Not Found.')

        return jsonify({'user': user.attributes})
    
    def delete(self, id):
        """
        Delete a gitlab user by their gitlab user id through the API.
        Requires admin privileges.
        :param id: the id of the gitlab user
        :return: The deleted user if found.
        """
        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        token = request.headers['Private-Token']

        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                gl.users.delete(id)

            return jsonify({'User deleted.'})

        except GitlabDeleteError as error:
            abort(204, 'Resource not found.')
        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')


class UserList(Resource):
    # Requires API privileges
    """
    UserList represents an API resource for users on gitlab.
    """
    def get(self):
        """
        Get the list of users from gitlab the current user is allowed to see.
        :return: The list of gitlab users.
        """
        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        token = request.headers['Private-Token']

        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                users = gl.users.list()
                userList = [user.attributes for user in users]
                
        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')

        return jsonify({'Users': userList})
