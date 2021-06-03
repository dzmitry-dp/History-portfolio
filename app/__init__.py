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

    position = {
        'opening_time': opening_time,
        'instrument': instrument,
        'amount': amount,
        'open_price': open_price,
    }
    return position
