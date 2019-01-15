import sys
sys.path.append('..')
from flask_restful import Resource
from flask import jsonify
import gitlab
from auth import repo_url

class Project(Resource):

    # Get a single project by project ID
    def get(self, id, token):
        with gitlab.Gitlab(repo_url, ssl_verify=False, private_token=token) as gl:
            project = gl.projects.get(id)
            return jsonify({"project": project.attributes})


