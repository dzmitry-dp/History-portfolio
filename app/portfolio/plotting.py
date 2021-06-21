import pandas as pd

from app.db.database import db
from app.parsing.yahoo import call_number
from config import history_table # имя таблицы исторических данных


class ResultPips:
    def __init__(self, portfolio_data):
        # for position in portfolio_data:
        #     print(position.opening_time)
        #     print(position.instrument)
        #     print(position.amount)
        #     print(position.open_price)

        self.portfolio_data = portfolio_data
        self.db_columns_list = [position.instrument.replace('/', '').lower() for position in portfolio_data]
        df_from_db = self.get_total_history_dataframe() # таблица данных по инструментам портфеля
        clear_df = self.clear_dataframe(df_from_db) # удаляю цены в столбцах позиций когда они еще не были открыты
        pips_df = self.get_pips_dataframe(clear_df) # вычисляю количество пунктов по каждой позиции в датафрейме
        # print(pips_df.sum(axis=1))
        self.draw_graph(pips_df)

    def get_first_date_time(self):
        date_time_list = [position.opening_time for position in self.portfolio_data]
        return min(date_time_list) # дата самой ранней позиции в портфеле

    def get_total_history_dataframe(self):
        from app import hist
        # print(f"SELECT {', '.join(columns)} FROM {history_table} WHERE `index` > '{idx_dt.strftime('%Y-%m-%d %H:%M:%S')}'")
        with hist.app_context():
            return pd.read_sql_query(
                f"SELECT `index`, {', '.join(self.db_columns_list)} \
                    FROM {history_table} \
                        WHERE `index` > '{self.get_first_date_time().strftime('%Y-%m-%d %H:%M:%S')}'",
                        con=db.engine,
                        index_col='index',
                        )
    
    def clear_dataframe(self, df):
        values = {}
        for position in self.portfolio_data:
            column = position.instrument.replace('/', '').lower()
            df[column] = \
                    df[column]\
                        .loc[position.opening_time.strftime('%Y-%m-%d %H:%M:%S'):]
            values[column] = position.open_price
        return df.fillna(value=values) # заполняю пропуски ценами открытия, т.к. в эти моменты времени позиция небыла открыта и pips = 0

    def get_pips_dataframe(self, df):
        for position in self.portfolio_data:
            column = position.instrument.replace('/', '').lower()
            if position.amount > 0:
                df[column] = \
                    (df[column] - position.open_price) *\
                        call_number[position.instrument]['coefficient'] *\
                            abs(position.amount)
            elif position.amount < 0:
                df[column] = \
                    (position.open_price - df[column]) *\
                        call_number[position.instrument]['coefficient'] *\
                            abs(position.amount)

        return df

    def draw_graph(self, data):
        plot = data.plot()
        fig = plot.get_figure()
        fig.savefig('app/static/img/result_pips.png')