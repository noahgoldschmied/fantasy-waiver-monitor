from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv() #loads the .env

YAHOO_CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
YAHOO_CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Fantasy Waiver Monitor!"

if __name__ == "__main__":
    app.run()
