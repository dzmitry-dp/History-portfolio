"""Модуль для накопления исторических данных о ценах инструментов"""

import pandas as pd
from threading import Thread

from app.db.database import db
from config import history_table # имя таблицы исторических данных


class ThreadHistoryPrices(Thread):
    _table_name = history_table # имя таблицы исторических данных
    
    def __init__(self, instrument, yahoo_df):
        Thread.__init__(self)
        self.instrument = instrument
        self.df = yahoo_df

    def run(self):
        from app import hist

        df_to_db = get_prices(self.df, self.instrument)

        with hist.app_context():
            try:
                df_from_db = read_history_price_from_database(self._table_name, db.engine)
                merged = merge_sql_dataframe_and_new_history_data(df_from_db, df_to_db)
                write_history_data_to_sql(
                    table_name = self._table_name, 
                    df_to_db = merged,
                    con = db.engine,
                    )
            except ValueError:
                print('Table not found ')
                write_history_data_to_sql(
                    table_name = self._table_name, 
                    df_to_db = df_to_db,
                    con = db.engine,
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