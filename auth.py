import sys
sys.path.append('..')
from flask import abort, request
import gitlab
import requests
repo_url = 'http://129.213.56.181'

#TODO: Implement cookie/JWT based authentication 
def getUserIdToken(token):
    try:

        with gitlab.Gitlab(repo_url, private_token=token, ssl_verify=False) as gl:
            gl.auth()
            current_user_id = gl.user.attributes['id']

        return current_user_id

    except GitlabAuthenticationError as error:
        abort(401, 'User Unauthorized.')

def getUserIdOauth(oauth_token):
    try:

        with gitlab.Gitlab(repo_url, oauth_token=oauth_token, ssl_verify=False) as gl:
            gl.auth()
            current_user_id = gl.user.attributes['id']

        return current_user_id

    except GitlabAuthenticationError as error:
        abort(401, 'User Unauthorized.')


"""
Validates authenticty of user's access token and returns their user id
from gitlab.

:param token: the gitlab API token
:return: The user's gitlab id if successful.
"""
def validate(token):
        headers = {'Private-Token': token}
        r = requests.get('https://gitlab.cloudsolutionhubs.com/api/v4/user', verify=False, headers=headers)

        if r.status_code != requests.codes.ok:
            print('validation failed')
            return None

        data = r.json()
        return data['id']


# Authentication Wrapper for routes 
# that don't naturally have validation/authentication via gitlab
"""
Authentication wrapper for routes that do not naturally require authentication
with gitlab.
:param func: the function to wrap with authentication
:return: The wrapped function
"""
def authenticate(func):
    def _wrap(*args, **kwargs):
        if 'Private-Token' not in request.headers:
            # No Token provided
            abort(401, 'User Unauthorized')
            return None

        print("Checking Token.")
        user_id = validate(request.headers['Private-Token'])

        if user_id is None:
            abort(401, 'User Unauthorized')
            return None

        return func(user_id=user_id, *args, **kwargs)
    return _wrap