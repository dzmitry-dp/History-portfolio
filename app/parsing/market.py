import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from app.parsing.yahoo import call_number
from app.db.history import ThreadHistoryPrices


class Market:
    def __init__(self, instrument, start, interval):
        self._data = yf.Ticker(call_number[instrument]['cipher'])
        self.coefficient = call_number[instrument]['coefficient']
        self.history_data = self.correct_index_to_datetime(
            self._data.history(
                interval=interval,
                start=start,
                )
            )
    
    def correct_index_to_datetime(self, data):
         # для того чтобы можно было сравнивать время
        data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S.%f')\
            .values.astype('datetime64[ns]')
        return data

def get_market(instrument, time_start, interval):
    market = Market(instrument=instrument, start=time_start, interval=interval)
    thread = ThreadHistoryPrices(instrument, market.history_data) # поток записи исторических данных
    thread.start()
    return market.history_data

def get_open_price(instrument, opening_time, direction):
    time_start = opening_time.strftime('%Y-%m-%d')
    passed = datetime.today() - opening_time # как давно открывается

    interval = '1h'
    data_index = opening_time - timedelta(minutes=opening_time.minute)

    if passed.days > 730:
        return None # ограничение для позиций старше 730 дней

    data = get_market(instrument=instrument, time_start=time_start, interval=interval)

    if direction == 'buy': # если покупаю, то по high (худший вариант)
        return data.loc[data_index]['High']
    elif direction == 'sell': # если продаю, то по low (худший вариант)
        return data.loc[data_index]['Low']

def get_new_position(form):
    opening_time = datetime.strptime(form['date'] + ' ' + form['time'], '%Y-%m-%d %H:%M')
    instrument = form['instrument']
    amount = form['amount']

    if int(amount) > 0:
        direction = 'buy'
    elif int(amount) <= 0:
        direction = 'sell'

    open_price = get_open_price(instrument, opening_time, direction)

    position = {
        'opening_time': opening_time,
        'instrument': instrument,
        'amount': amount,
        'open_price': open_price,
    }
    return position