from flask import Blueprint, render_template, request
from app.forms import NewOpenPositionForm, PortfolioForm
from app import add_new_position, get_portfolio_name_from_file
import pickle
import app.db_models as db_models


portfolio = Blueprint('portfolio', __name__, template_folder='templates')

@portfolio.route('/portfolio', methods=['POST', 'GET'])
def add_position():
    position_form = NewOpenPositionForm()
    portfolio_form = PortfolioForm()
    if request.method == 'POST':
        position_to_add = add_new_position(request.form)
        position_to_db = db_models.Position(
            opening_time=position_to_add['opening_time'],
            instrument=position_to_add['instrument'],
            amount=position_to_add['amount'],
            open_price=position_to_add['open_price'],
        )
        db_models.db.session.add(position_to_db)
        db_models.db.session.commit()
    return render_template('main.html', position_form=position_form, portfolio_form=portfolio_form)

@portfolio.route('/', methods=['POST', 'GET'])
def show_portfolio():
    position_form = NewOpenPositionForm()
    portfolio_form = PortfolioForm()
    if request.method == 'POST':
        portfolio_name = request.form['portfolio_name']
        with open('app/portfolio/name', 'wb') as file:
            pickle.dump(portfolio_name, file)
        
        positions = db_models.Position.query.all()
        print(positions)
    return render_template('main.html', position_form=position_form, portfolio_form=portfolio_form)
