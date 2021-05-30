from wtforms import Form, StringField, DateTimeField, IntegerField, SelectField


class NewPositionForm(Form):
    date_time = DateTimeField(label='Date and Time', format='%m/%d/%y')
    instrument = StringField(label='Instrument')
    amount = IntegerField(label='Amount')
    portfolio = SelectField(label='Portfolio', choices=[
    	('portfolio_1', 'portfolio_1'), 
    	('portfolio_2', 'portfolio_2'), 
        ])