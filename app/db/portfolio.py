"""Модуль для хранения данных о портфолио"""

from app.db.database import db


class Position(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    opening_time = db.Column(db.DateTime)
    instrument = db.Column(db.String(14)) # ограничение в 14 символов
    amount = db.Column(db.Integer)
    open_price = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        super(Position, self).__init__(*args, **kwargs)
        db.create_all()

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Opening_time: {self.opening_time} Instrument: {self.instrument} Amount: {self.amount} Price_open: {self.open_price}'


def write_position_to_database(position):
    position_to_db = Position(
        opening_time=position['opening_time'],
        instrument=position['instrument'],
        amount=position['amount'],
        open_price=position['open_price'],
    )
    db.session.add(position_to_db)
    db.session.commit()

def read_portfolio_table_from_database():
    positions = Position.query.all()
    return positions

def remove_position_from_database(primapy_key):
    del_obj = Position.query.filter_by(id=primapy_key).first()
    db.session.delete(del_obj)
    db.session.commit() 
