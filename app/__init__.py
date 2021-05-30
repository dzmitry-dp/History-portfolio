from flask import Flask


def create_app(name=__name__):
    app = Flask(__name__)
    return app

def add_new_position(form):
    date = form['date']
    time = form['time']
    instrument = form['instrument']
    amount = form['amount']
    portfolio = form['portfolio']
    print(date, time, instrument, amount, portfolio)