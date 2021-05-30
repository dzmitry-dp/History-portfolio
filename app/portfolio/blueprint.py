from flask import Blueprint, render_template, request
from app.forms import NewPositionForm


portfolio = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio.route('/', methods=['POST', 'GET'])
def add_position():
    form = NewPositionForm()
    if request.method == 'POST':
        date_time = request.form['date_time']
        instrument = request.form['instrument']
        amount = request.form['amount']
        portfolio = request.form['portfolio']
        print(date_time, instrument, amount, portfolio)
        return render_template('add_position.html', form=form)
    return render_template('add_position.html', form=form)
