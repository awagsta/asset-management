import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
from auth import repo_url


# Get a single project by ID
class Project(Resource):
    def get(self, id):

        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        token = request.headers['Private-Token']

        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                project = gl.projects.get(id)

        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')

        return jsonify({"project": project.attributes})

# Get all existing projects.
class AllProjects(Resource):
    def get(self):

        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        token = request.headers['Private-Token']

        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                projects = gl.projects.get()
                projectList = [project.attributes for project in projects]

        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')

        return jsonify({"Projects": projectList})

# Get a List of all projects by a user.
class Project_List(Resource):
    def get(self):

        if 'Private-Token' not in request.headers:
            abort(401, 'User Unauthorized')

        token = request.headers['Private-Token']

        try:

            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                
                projects = gl.projects.list(owned=True)
                projectList = [project.attributes for project in projects]

        except GitlabAuthenticationError as error:
            abort(401, 'User Unauthorized.')

        return jsonify({"Projects": projectList})
        
