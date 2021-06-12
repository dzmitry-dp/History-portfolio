from wtforms import Form, StringField
from wtforms.validators import ValidationError, DataRequired
from wtforms.fields.html5 import DateField, TimeField, IntegerField
from datetime import datetime, timedelta

from app.parsing.yahoo import call_number


def validation_date(form, date):
    if date.data >= datetime.today().date() or date.data < datetime.today().date() - timedelta(days = 730):
        raise ValidationError('Not suitable date!')

def validation_instrument(form, instrument):
    if instrument.data not in call_number.keys():
        raise ValidationError('Unknown instrument!')

class NewOpenPositionForm(Form):
    date = DateField(label='Date', format='%Y-%m-%d', default=datetime.today, validators=[validation_date])
    time = TimeField(label='Time', format='%H:%M', default=datetime.now().time)
    instrument = StringField(label='Instrument', default='AUD/CAD', validators=[validation_instrument, DataRequired()])
    amount = IntegerField(label='Amount', default=0, validators=[DataRequired('Must be non-zero!')])
