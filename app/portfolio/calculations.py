import pandas as pd

from app.db.database import db
from app.parsing.yahoo import call_number
from config import history_table # имя таблицы исторических данны


def get_plotting_dataframe(portfolio_data):
    columns_list = [position.instrument.replace('/', '').lower() for position in portfolio_data]
    date_time_list = [position.opening_time for position in portfolio_data]
    df_from_db = get_total_history_dataframe_from_db(columns_list, date_time_list) # таблица данных по инструментам портфеля
    clear_df = cleaning_dataframe(portfolio_data, df_from_db) # удаляю цены в столбцах позиций когда они еще не были открыты
    pips_df = get_pips_dataframe(portfolio_data, clear_df) # вычисляю количество пунктов по каждой позиции в датафрейме
    return pips_df

def get_total_history_dataframe_from_db(columns_list, date_time_list):
    from app import hist

    with hist.app_context():
        return pd.read_sql_query(
            f"SELECT `index`, {', '.join(columns_list)} \
                FROM {history_table} \
                    WHERE `index` > '{min(date_time_list).strftime('%Y-%m-%d %H:%M:%S')}'",
            con=db.engine,
            index_col='index',
            )

def cleaning_dataframe(portfolio_data, df):
    values = {}
    for position in portfolio_data:
        column = position.instrument.replace('/', '').lower()
        df[column] = \
                df[column]\
                    .loc[position.opening_time.strftime('%Y-%m-%d %H:%M:%S'):]
        values[column] = position.open_price
    return df.fillna(value=values) # заполняю пропуски ценами открытия, т.к. в эти моменты времени позиция небыла открыта и pips = 0

def get_pips_dataframe(portfolio_data, df):
    for position in portfolio_data:
        column = position.instrument.replace('/', '').lower()
        if position.amount > 0:
            df[column] = (df[column] - position.open_price) *\
                            call_number[position.instrument]['coefficient'] *\
                                abs(position.amount)
        elif position.amount < 0:
            df[column] = (position.open_price - df[column]) *\
                            call_number[position.instrument]['coefficient'] *\
                                abs(position.amount)
    return df