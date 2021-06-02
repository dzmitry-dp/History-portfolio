from flask import Blueprint, render_template, request

from app import get_new_position, save_portfolio_name_to_file
from app.forms import NewOpenPositionForm, PortfolioForm
from app.db_models import write_position_to_database, read_table_from_database


portfolio = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio.route('/current_portfolio', methods=['POST', 'GET'])
def add_position():
    position_form = NewOpenPositionForm()
    portfolio_form = PortfolioForm()
    if request.method == 'POST':
        position_to_add = get_new_position(request.form)
        write_position_to_database(position_to_add)
    return render_template('main.html', position_form=position_form, portfolio_form=portfolio_form)

@portfolio.route('/new_portfolio', methods=['POST', 'GET'])
def show_portfolio():
    position_form = NewOpenPositionForm()
    portfolio_form = PortfolioForm()
    if request.method == 'POST':
        portfolio_name = save_portfolio_name_to_file(request.form['portfolio_name'])
        read_table_from_database(portfolio_name) # таблица == portfolio
    return render_template('main.html', position_form=position_form, portfolio_form=portfolio_form)
