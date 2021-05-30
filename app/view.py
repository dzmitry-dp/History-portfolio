from app import add_new_position
from app.hist_app import hist
from flask import render_template, request, redirect, url_for
from app.forms import NewOpenPositionForm


@hist.route("/", methods=['POST', 'GET'])
def index():
    form = NewOpenPositionForm()
    if request.method == 'POST':
        add_new_position(request.form)
        return redirect(url_for('portfolio.add_position'))
    return render_template('index.html', form=form)