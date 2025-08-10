from flask import Flask, redirect, request, session, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv() #loads the .env

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")


YAHOO_CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
YAHOO_CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")
REDIRECT_URI = "https://fantasy-waiver-monitor-0c72c9149be3.herokuapp.com/callback"

AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"

@app.route("/")
def home():
    return "Hello, Fantasy Waiver Monitor!"

@app.route("/login")
def login():
    params = {
        "client_id":YAHOO_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "fspt-w"
    }
    url = requests.Request('GET', AUTH_URL, params=params).prepare().url
    return redirect(url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code provided", 400

    data = {
        "client_id": YAHOO_CLIENT_ID,
        "client_secret": YAHOO_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code"
    }
    headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    token_response = requests.post(TOKEN_URL, data=data, headers=headers)

    if token_response.status_code != 200:
        return f"Failed to get token: {token_response.text}", 400

    token_json = token_response.json()
    session['access_token'] = token_json.get("access_token")

    return f"Access token acquired! Token: {session['access_token']}"

@app.route("/test-api")
def test_api():
    access_token = session.get("access_token")
    if not access_token:
        return "No access token found. Please /login first.", 401

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Example API call: Get user's fantasy NFL teams
    url = "https://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nfl/teams"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"API call failed: {response.status_code} {response.text}", 400

    return jsonify(response.json())

if __name__ == "__main__":
    app.run()
