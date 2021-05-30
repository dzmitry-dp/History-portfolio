from app import create_app
from config import FlaskHistConfiguration
from app.portfolio.blueprint import portfolio

hist = create_app()
hist.config.from_object(FlaskHistConfiguration)
hist.register_blueprint(portfolio, url_prefix='/add')