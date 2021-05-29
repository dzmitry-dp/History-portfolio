from app.hist_app import hist
from flask import render_template


@hist.route("/")
def index():
    return render_template('index.html')