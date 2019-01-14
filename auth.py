import gitlab
repo_url = 'https://129.213.56.181'

#TODO: Implement cookie/JWT based authentication 
def getUserId(url, token):
     with gitlab.Gitlab(repo_url, token) as gl:
        gl.auth()
        current_user_id = gl.user.attributes.id
        return current_user_id
