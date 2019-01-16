import sys
sys.path.append('..')
import gitlab
repo_url = 'https://gitlab.cloudsolutionhubs.com'

#TODO: Implement cookie/JWT based authentication 
def getUserIdToken(token):
     with gitlab.Gitlab(repo_url, private_token=token, ssl_verify=False) as gl:
        gl.auth()
        current_user_id = gl.user.attributes.id
        return current_user_id

def getUserIdOauth(oauth_token):
    with gitlab.Gitlab(repo_url, oauth_token=oauth_token, ssl_verify=False) as gl:
        gl.auth()
        current_user_id = gl.user.attributes.id
        return current_user_id
