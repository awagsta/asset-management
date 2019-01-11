import gitlab
repo_url = 'www.gitlab.com'

def auth(url, token):
     with gitlab.Gitlab(repo_url, token) as gl:
        gl.auth()
        current_user_id = gl.user.attributes.id
    return current_user_id
