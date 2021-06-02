import pickle
from flask import Flask
from datetime import datetime

from app.parsing import get_open_price


def create_app(name=__name__):
    app = Flask(__name__)
    return app

def get_new_position(form):
    opening_time = datetime.strptime(form['date'] + ' ' + form['time'], '%Y-%m-%d %H:%M')
    instrument = form['instrument']
    amount = form['amount']
    open_price = get_open_price(instrument)
    # portfolio_name = form['portfolio_name']

    position = {
        'opening_time': opening_time,
        'instrument': instrument,
        'amount': amount,
        'open_price': open_price,
        # 'portfolio': portfolio_name,
    }
    return position

def save_portfolio_name_to_file(name):
    with open('app/portfolio/name', 'wb') as file:
        pickle.dump(name, file)
    return name

def get_portfolio_name_from_file():
    with open('app/portfolio/name', 'rb') as file:
        name = pickle.load(file)
    return name