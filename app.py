import os

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from pymongo import MongoClient
from requests_oauthlib import OAuth2Session

load_dotenv()

OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
OAUTH2_REDIRECT_URI = os.getenv("REDIRECT_URI")

API_BASE_URL = os.environ.get("API_BASE_URL", "https://discord.com/api")
AUTHORIZATION_BASE_URL = API_BASE_URL + "/oauth2/authorize"
TOKEN_URL = API_BASE_URL + "/oauth2/token"

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = OAUTH2_CLIENT_SECRET

if OAUTH2_REDIRECT_URI.startswith("http://"):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

if OAUTH2_REDIRECT_URI.startswith("https://"):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"

cluster = MongoClient(os.getenv("MONGODB_URL"))

guestbook = cluster["dagelan"]["guestbook"]


def token_updater(token):
    session["oauth2_token"] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            "client_id": OAUTH2_CLIENT_ID,
            "client_secret": OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/authorize/")
def auth():
    scope = request.args.get("scope", "identify")
    discord = make_session(scope=scope.split(" "))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session["oauth2_state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    if request.values.get("error"):
        return request.values["error"]
    discord = make_session(state=session.get("oauth2_state"))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url,
    )
    session["oauth2_token"] = token

    # get the user object from discord api
    user = discord.get(API_BASE_URL + "/users/@me").json()

    # then take what we need
    user_id = user["id"]
    username = user["username"]
    discrim = user["discriminator"]

    # first, find if user already registered or not
    user_in_db = guestbook.find_one({"uid": user_id})

    # checks
    if user_in_db is None:
        # if user never goes through verification, return error 400
        return abort(400)
    else:
        # if user is in our discord server, change the status to True inside database
        guestbook.update_one({"uid": member.id}, {"$set": {"verified": True}})
        # redirect user to the "done" page
        return redirect(url_for("authorized"))


@app.route("/authorized/")
def authorized():
    return render_template("done.html")


if __name__ == "__main__":
    app.run()
