from flask import Blueprint, render_template, request

from app import get_new_position
from app.forms import NewOpenPositionForm
from app.db_models import write_position_to_database, read_table_from_database, remove_position_from_database


portfolio = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio.route('/added', methods=['POST', 'GET'])
def add_position():
    position_form = NewOpenPositionForm()
    if request.method == 'POST':
        position_to_add = get_new_position(request.form)
        write_position_to_database(position_to_add)
        portfolio_data = read_table_from_database()
    return render_template('main.html', position_form=position_form, portfolio_data=portfolio_data)

@portfolio.route('/removed', methods=['POST', 'GET'])
def remove_position():
    position_form = NewOpenPositionForm()
    if request.method == 'POST':
        remove_position_from_database(request.form['del'])
        portfolio_data = read_table_from_database() 
    return render_template('main.html', position_form=position_form, portfolio_data=portfolio_data)