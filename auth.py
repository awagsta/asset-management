import sys
sys.path.append('..')
from flask import abort
import gitlab
import requests
repo_url = 'https://gitlab.cloudsolutionhubs.com'

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


#Validates authenticity of token and returns user id.
def validate(token):
        headers = {'Private-Token': token}
        r = requests.get('https://gitlab.cloudsolutionhubs.com/api/v4/user', verify=False, headers=headers)

        if r.status_code != requests.codes.ok:
            print('validation failed')
            return none

        data = r.json()
        return data['id']


# Authentication Wrapper for routes 
# that don't naturally have validation/authentication via gitlab
def authenticate(func):
    def _wrap(*args, **kwargs):
        if 'Private-Token' not in request.headers:
            # No Token provided
            abort(401, 'User Unauthorized')
            return None

        print("Checking Token.")
        id = validate(request.headers['Private-Token'])

        if id is None:
            abort(401, 'User Unauthorized')
            return None

        return func(id=id, *args, **kwargs)
    return _wrap