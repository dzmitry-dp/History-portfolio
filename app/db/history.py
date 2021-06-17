"""Модуль для накопления исторических данных о ценах инструментов"""

import pandas as pd
from threading import Thread

from app.db.database import db

class ThreadHistoryPrices(Thread):
    def __init__(self, instrument, yahoo_df):
        Thread.__init__(self)
        self.instrument = instrument
        self.df = yahoo_df
        self.table_name = 'm_test'

    def run(self):
        df_to_db = get_prices(self.df, self.instrument)
        from app import hist
        with hist.app_context():
            df_from_db = read_history_price_from_database(self.table_name, db.engine)
            write_history_data_to_sql(
                self.table_name, 
                merge_sql_dataframe_and_new_history_data(df_from_db, df_to_db),
                db.engine,
                )


def write_history_data_to_sql(table_name, df_to_db, con):
    df_to_db.to_sql(name=table_name, con=con, if_exists='replace', index=True)

def read_history_price_from_database(table_name, con):
    return pd.read_sql_table(table_name=table_name, con=con, index_col='index')

def merge_sql_dataframe_and_new_history_data(sql_table, new_df):
    if new_df.columns[0] not in sql_table.columns:
        return pd.concat([sql_table, new_df], axis=1)
    else:
        return sql_table.combine_first(new_df)

def get_prices(df, instrument):
    df_to_db = (df['High'] + df['Low'])/2
    df_to_db = df_to_db.to_frame()
    df_to_db.rename(columns={0: instrument.replace('/', '').lower()}, inplace=True)
    return df_to_db