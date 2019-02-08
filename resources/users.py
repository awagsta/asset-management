import sys
sys.path.append('..')
from flask_restful import Resource
from flask import request, abort, url_for, jsonify
from marshmallow import fields
from webargs.flaskparser import use_args
from auth import repo_url
import gitlab
from gitlab.exceptions import *

# add user lookup to ensure user does not already exist.

#webargs expected fields for user creation
user_args = {
    'email': fields.Email(required=True),
    'password': fields.Str(required=True),
    'username': fields.Str(required=True),
    'name': fields.Str(required=True)
}

class User(Resource):
    # This route requires API privileges
    """
    User represents an API resource for a user on gitlab.
    """
    @use_args(user_args)
    def post(self, args):
        """
        Create a gitlab user through the API. Requires admin privileges.
        :param args: user args retrieved from the POST body
        :return: The created user.
        """

        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        user = {
            'email': args['email'],
            'password': args['password'],
            'username': args['username'],
            'name': args['name']
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