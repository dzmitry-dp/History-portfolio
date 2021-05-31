from app.hist_app import hist
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(hist)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opening_time = db.Column(db.DateTime)
    instrument = db.Column(db.String(14)) # ограничение в 14 символов
    amount = db.Column(db.Integer)
    open_price = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        super(Position, self).__init__(*args, **kwargs)