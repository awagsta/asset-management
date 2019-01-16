import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify
import gitlab
from gitlab.exceptions import GitlabAuthorizationException
from auth import repo_url

# Get a single project by ID
class Project(Resource):
    def get(self, id, token):
        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                project = gl.projects.get(id)

        except GitlabAuthorizationException as error:
            abort(403, 'User Unauthorized.')

        return jsonify({"project": project.attributes})

# Get all existing projects.
class AllProjects(Resource):
    def get(self, token):
        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                projects = gl.projects.get()
                projectList = []

                for project in projects:
                    projectList.append({"project": project.attributes})

        except GitlabAuthorizationException as error:
            abort(403, 'User Unauthorized.')

        return jsonify({"Projects": projectList})

# Get a List of all projects by a user.
class Project_List(Resource):
    def get(self, id, token):
        try:
            with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
                projects = gl.projects.get(id)
                projectList = []

                for project in projects:
                    projectList.append({"project": project.attributes})

        except GitlabAuthorizationException as error:
            abort(403, 'User Unauthorized.')
        
        return jsonify({"Projects": projectList})
        
