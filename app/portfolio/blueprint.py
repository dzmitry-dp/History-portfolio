from flask import Blueprint, render_template, request

from app.forms import NewOpenPositionForm
from app.portfolio import plotting
from app.db.portfolio import write_position_to_database, read_portfolio_table_from_database, remove_position_from_database
from app.portfolio.calculations import get_plotting_dataframe
from app.parsing import market

portfolio = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio.route('/added', methods=['POST', 'GET'])
def add_position():
    position_form = NewOpenPositionForm(request.form)
    if request.method == 'POST' and position_form.validate():
        position_to_add = market.get_new_position(request.form)
        write_position_to_database(position_to_add)
    portfolio_data = read_portfolio_table_from_database() # таблица данных из DB
    return render_template('main.html', position_form=position_form, portfolio_data=portfolio_data)

@portfolio.route('/removed', methods=['POST'])
def remove_position():
    position_form = NewOpenPositionForm()
    if request.method == 'POST':
        remove_position_from_database(request.form['del'])
        portfolio_data = read_portfolio_table_from_database() 
    return render_template('main.html', position_form=position_form, portfolio_data=portfolio_data)

@portfolio.route('/result', methods=['POST'])
def show_portfolio_result():
    position_form = NewOpenPositionForm()
    portfolio_data = read_portfolio_table_from_database() 
    df_for_plotting = get_plotting_dataframe(portfolio_data)
    plotting.draw_result_pips_graph(df_for_plotting)
    return render_template('result.html', position_form=position_form, portfolio_data=portfolio_data)