import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from app.parsing.yahoo import call_number


class Market:
    def __init__(self, instrument, start, end, interval):
        self._data = yf.Ticker(call_number[instrument]['cipher'])
        self.coefficient = call_number[instrument]['coefficient']
        self.history_data = self._data.history(
            interval=interval,
            start=start,
            end=end,
        )

def get_open_price(instrument, opening_time, direction):
    time_start = opening_time.strftime('%Y-%m-%d')
    time_end = (opening_time + timedelta(days=1)).strftime('%Y-%m-%d') # скачиваем данные за сутки
    passed = datetime.today() - opening_time # как давно открывается

    # if passed.days < 30:
    #     interval = '1m'
    #     data_index = opening_time
    # elif 30 < passed.days < 730:
    #     interval = '1h'
    #     data_index = opening_time - timedelta(minutes=opening_time.minute)
    # else: # ограничение для позиций старше 730 дней
    #     return None

    interval = '1h'
    if passed.days > 730:
        return None # ограничение для позиций старше 730 дней

    market = Market(instrument=instrument, start=time_start, end=time_end, interval=interval)
    data = market.history_data
    # для того чтобы можно было сравнивать время
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S.%f')\
        .values.astype('datetime64[ns]')

    if direction == 'buy': # если покупаю, то по high (худший вариант)
        return data.loc[data_index]['High']
    elif direction == 'sell':
        return data.loc[data_index]['Low']
