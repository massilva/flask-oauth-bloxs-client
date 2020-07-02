from flask import url_for, session
from flask import render_template, redirect, abort, Flask
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = '!secret'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

BASE_URL = 'http://localhost:80'

CONF_URL = {
 "issuer": BASE_URL,
 "authorization_endpoint": BASE_URL + "/oauth2/authorize",
 "device_authorization_endpoint": BASE_URL + "/device/code",
 "token_endpoint": BASE_URL + "/token",
 "userinfo_endpoint": BASE_URL + "/me",
 "revocation_endpoint": BASE_URL + "/revoke",
 "response_types_supported": [
  "code",
  "token",
  "id_token",
  "code token",
  "code id_token",
  "token id_token",
  "code token id_token",
  "none"
 ],
 "subject_types_supported": [
  "public"
 ],
 "id_token_signing_alg_values_supported": [
  "RS256"
 ],
 "scopes_supported": [
  "project",
  "email",
  "profile"
 ],
 "token_endpoint_auth_methods_supported": [
  "client_secret_post",
  "client_secret_basic"
 ],
 "claims_supported": [
  "aud",
  "email",
  "email_verified",
  "exp",
  "family_name",
  "given_name",
  "iat",
  "iss",
  "locale",
  "name",
  "picture",
  "sub"
 ],
 "code_challenge_methods_supported": [
  "plain",
  "S256"
 ],
 "grant_types_supported": [
  "authorization_code",
  "refresh_token",
 ]
}

oauth = OAuth(app)
oauth.register(
    name='bloxs',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'project email profile'
    }
)

'''
def normalize_twitter_userinfo(client, data):
    # make twitter account data into UserInfo format
    params = {
        'sub': data['id_str'],
        'name': data['name'],
        'email': data.get('email'),
        'locale': data.get('lang'),
        'picture': data.get('profile_image_url_https'),
        'preferred_username': data.get('screen_name'),
    }
    username = params['preferred_username']
    if username:
        params['profile'] = 'https://twitter.com/{}'.format(username)
    return params


oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    userinfo_endpoint='account/verify_credentials.json?include_email=true&skip_status=true',
    userinfo_compliance_fix=normalize_twitter_userinfo,
    fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)
'''

@app.route('/')
def homepage():
    user = session.get('user')
    print('user', user)
    return render_template('home.html', user=user)


@app.route('/login/<name>')
def login(name):
    client = oauth.create_client(name)
    if not client:
        abort(404)

    redirect_uri = url_for('auth', name=name, _external=True)
    return client.authorize_redirect(redirect_uri)


@app.route('/auth/<name>')
def auth(name):
    client = oauth.create_client(name)
    if not client:
        abort(404)

    token = client.authorize_access_token()
    if 'id_token' in token:
        user = client.parse_id_token(token)
    else:
        user = client.userinfo()

    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
