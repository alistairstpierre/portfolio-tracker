from asyncio.windows_events import NULL
import collections
from flask import Flask, render_template, request
import os
import json
import sys

from helpers import lookup

app = Flask(__name__)

# Make sure API key is set
# use [System.Environment]::SetEnvironmentVariable('ResourceGroup','AZ_Resource_Group')
if not os.environ.get("API_PORTFOLIO_TRACKER"):
   raise RuntimeError("API_KEY not set")

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
    print('inside virtualenv or venv')
else:
    print('outside virtualenv or venv')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # check for valid input
        req = request.form.get("hidden")
        if req == None:
            return render_template('index.html')
        data = lookup(req)
        if data == None:
            return render_template('index.html')
        # get image from data and display it
        return render_template('index.html', nfts=data['nfts'], collections=data['collections'])
    return render_template('index.html')