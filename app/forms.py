from wtforms import Form, StringField, SelectField
from wtforms.fields.html5 import DateField, TimeField, IntegerField
from datetime import datetime


class NewOpenPositionForm(Form):
    date = DateField(label='Date', format='%Y-%m-%d', default=datetime.today)
    time = TimeField(label='Time', format='%H:%M', default=datetime.now().time)
    instrument = StringField(label='Instrument', default='AUD/CAD')
    amount = IntegerField(label='Amount', default=0)
    portfolio_name = StringField(label='Portfolio', default='portfolio_1')


class PortfolioForm(Form):
    portfolio_name = StringField(label='Portfolio', default='portfolio_1')