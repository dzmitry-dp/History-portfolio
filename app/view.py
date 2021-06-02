from app import add_new_position
from app.hist_app import hist
from flask import render_template, request, redirect, url_for
from app.forms import NewOpenPositionForm, PortfolioForm


@hist.route("/", methods=['POST', 'GET'])
# выбор портфолио?
def select_portfolio():
    portfolio_form = PortfolioForm()
    if request.method == 'POST':
        return redirect(url_for('portfolio.add_position'))
    return render_template('index.html', portfolio_form=portfolio_form)