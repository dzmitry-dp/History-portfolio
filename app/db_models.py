from app import hist_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(hist_app.hist)

class Position(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    opening_time = db.Column(db.DateTime)
    instrument = db.Column(db.String(14)) # ограничение в 14 символов
    amount = db.Column(db.Integer)
    open_price = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        super(Position, self).__init__(*args, **kwargs)
        # self.create_table()

    def create_table(self):
        db.create_all()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Opening_time: {self.opening_time} Instrument: {self.instrument} Amount: {self.amount} Price_open: {self.open_price}'