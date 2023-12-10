"""
cleveroauth
A Clever OAuth2.0 Example

© 2023 - now, de-y
"""

from flask import *
import jwt, requests
import dotenv

c = dotenv.dotenv_values(".env")

app = Flask(__name__, template_folder='./pages')

l_url = f'https://clever.com/oauth/authorize?response_type=code&client_id={c['CLEVER_CID']}&redirect_uri={c['CLEVER_RURI']}'

@app.route('/')
def index():
    return render_template('index.html', clever_login_url = l_url)

@app.route('/oauth/clever')
def clever_oauth():
    """
    Path: /oauth/clever
    Oauth the User with Clever API.
    """
    c_info = requests.post('https://clever.com/oauth/tokens', data = {
        'code': request.args.get('code'),
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:3000/oauth/clever',
        'client_id': c['CLEVER_CID'],
        'client_secret': c['CLEVER_CSECRET']
    }).json()
    # Above line gets the access token from the Clever API

    l_info = requests.get('https://api.clever.com/me', headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {c_info['access_token']}'})
    # Above line gets the User ID for use to get user info from the clever API

    user_information = requests.get(f'https://api.clever.com/v3.0/users/{l_info.json()['data']['id']}', headers = {"accept": "application/json",'authorization': f'Bearer {c_info['access_token']}'}).json()
    # Above requests gets the user information, the email and full name from the Clever API.
    
    district_information = requests.get(f'https://api.clever.com/v3.0/districts/{user_information['data']['district']}', headers = {"accept": "application/json",'authorization': f'Bearer {c_info['access_token']}'}).json()['data']['name']
    # Above requests gets the District Information, the name from the Clever API.
    
    token = jwt.encode({'data': {'email': user_information['data']['email'],'full_name': f'{user_information['data']['name']['first']} {user_information['data']['name']['middle']} {user_information['data']['name']['last']}'}, 'district_name': district_information}, c['JWT_SECRET'], algorithm='HS256')
    # Above code encodes the JWT.
    
    # resp = make_response({'message': {'email': user_information['data']['email'],'full_name': f'{user_information['data']['name']['first']} {user_information['data']['name']['middle']} {user_information['data']['name']['last']}', 'district_name': district_information}})
    # Above code makes the response.        
    # make_response(redirect('/')).set_cookie('sid', token, expires='session')
    # Above code sets the cookie with JWT token.
    r =  make_response(redirect('/user'))
    r.set_cookie('sid', token, expires='session')
    return r

@app.route('/user')
def user():
    """
    Path: /user
    User Page
    """
    try:
        token = request.cookies.get('sid')
        print(token)
        if token == None:
            return redirect('/')
        else:
            data = jwt.decode(token, c['JWT_SECRET'], algorithms=['HS256'])
            return render_template('user.html', email = data['data']['email'], full_name = data['data']['full_name'], district_name = data['district_name'])
    except Exception as e:
        print(e)
        return redirect('/')

@app.route('/logout')
def logout():
    """
    Path: /logout
    Logout the User
    """
    resp = make_response(redirect('/'))
    resp.delete_cookie('sid')
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=3000)