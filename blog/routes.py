from blog import app
from flask import render_template, request

@app.route('/')
def homepage():
    return render_template("base.html")
