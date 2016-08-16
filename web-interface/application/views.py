from flask import render_template

from . import app


@app.route('/')
def route_index():
    return render_template("base.html")
