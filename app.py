from flask import Flask, render_template, request
import os

from helpers import lookup

app = Flask(__name__)

# Make sure API key is set
# use [System.Environment]::SetEnvironmentVariable('ResourceGroup','AZ_Resource_Group')
if not os.environ.get("API_PORTFOLIO_TRACKER"):
   raise RuntimeError("API_KEY not set")

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        lookup()

    return render_template('index.html')