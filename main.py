import requests

from flask import Flask, render_template, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from helpers import config, decode_token
from user import User


app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})

login_manager = LoginManager()
login_manager.init_app(app)


NONCE = 'ThisIsASampleNonce'
STATE = 'ThisIsASampleState'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    vc = request.args.get("vc")
    scope = "openid vc_authn" if vc else "openid profile identity_card"

    # get request params
    query_params = {'client_id': config["client_id"],
                    'scope': scope,
                    'nonce': NONCE,
                    'state': STATE,
                    'response_type': 'code',
                    'redirect_uri': 'http://localhost:8081/callback'}

    if vc:
        query_params.update({'pres_req_conf_id': 'verified-email'})

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=config["auth_uri"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': 'http://localhost:8081/callback'}
    query_params = requests.compat.urlencode(query_params)
    response = requests.post(
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    )
    if not response.ok:
        return f"Error calling token endpoint: {response.text}", 403

    response_data = response.json()

    # Get tokens
    if response_data.get("token_type") != 'Bearer':
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = response_data["access_token"]
    id_token_decoded = decode_token(response_data["id_token"])
    if id_token_decoded is None:
        return "Invalid id token.", 403

    # Get userinfo
    # userinfo_response = requests.get(config["userinfo_uri"],
    #                                  headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = id_token_decoded["sub"]
    username = id_token_decoded["preferred_username"] if "preferred_username" in id_token_decoded else unique_id
    email = id_token_decoded["email"] if "email" in id_token_decoded else None
    id_card_info = id_token_decoded['documents'][0] if "documents" in id_token_decoded else None
    user = User(id_=unique_id, username=username,
                identity_card_info=id_card_info,
                email=email)

    if not User.get(unique_id):
        User.create(unique_id, username, id_card_info, email)

    login_user(user)
    return redirect(url_for("profile"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="localhost", port=8081)
