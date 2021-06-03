from flask import render_template, request, redirect, url_for

from app.hist_app import hist
from app.forms import NewOpenPositionForm
from app.db_models import read_table_from_database


@hist.route("/", methods=['POST', 'GET'])
def get_started():
    position_form = NewOpenPositionForm()
    portfolio_data = read_table_from_database() 
    return render_template('index.html', position_form=position_form, portfolio_data=portfolio_data)