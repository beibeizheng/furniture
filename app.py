from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


