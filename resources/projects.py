import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify, abort, request
import gitlab
from gitlab.exceptions import GitlabAuthenticationError
from auth import repo_url


# Get a single project by ID
class Project(Resource):
    """
    Project represents an API resource for projects on gitlab.
    """
    def get(self, id):
        """
        Get a project and it's associated details from gitlab.
        :param id: the id of the gitlab project to retrieve
        :return: the project.
        """

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
    """
    AllProjects represents an API resource for all projects on gitlab.
    """
    def get(self):
        """
        Get all projects from gitlab the current user is allowed to view.
        :return: the list of projects the user can see.
        """

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
    """
    ProjectList represents an API resource for all projects associated
    with the current user.
    """
    def get(self):
        """
        Get all projects from gitlab associated with the current user.
        :return: a list of the current user's gitlab projects
        """

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