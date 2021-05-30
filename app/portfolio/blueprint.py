from flask import Blueprint, render_template, request
from app.forms import NewOpenPositionForm
from app import add_new_position


portfolio = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio.route('/', methods=['POST', 'GET'])
def add_position():
    form = NewOpenPositionForm()
    if request.method == 'POST':
        add_new_position(request.form)
    return render_template('add_position.html', form=form)
