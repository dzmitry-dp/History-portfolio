import pandas as pd

from app.parsing.market import Market
from app.db.portfolio import db


def write_history_data_to_sql(table_name, df_to_db, con=db.engine):
    df_to_db.to_sql(name=table_name, con=con, if_exists='replace', index=True)

def read_history_price_from_database(table_name, con=db.engine):
    return pd.read_sql_table(table_name=table_name, con=con, index_col='index')

def merge_sql_dataframe_and_new_history_data(sql_table, new_df):
    if new_df.columns[0] not in sql_table.columns:
        return pd.concat([sql_table, new_df], axis=1)
    else:
        return sql_table.combine_first(new_df)

def get_prices_from_yahoo(instrument, time_start, time_end, interval):

    "instrument = 'AUD/CAD', time_start = '2021-06-10', time_end = '2021-06-11', interval = '1h'"
    
    market = Market(instrument, time_start, time_end, interval)
    df = market.history_data
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S.%f')\
            .values.astype('datetime64[ns]')
    df_to_db = (df['High'] + df['Low'])/2
    df_to_db = df_to_db.to_frame()
    df_to_db.rename(columns={0: instrument.replace('/', '').lower()}, inplace=True)
    return df_to_db