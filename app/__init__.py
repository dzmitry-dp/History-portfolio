from flask import Flask

from app.db.database import db
from config import FlaskHistConfiguration


def create_app(name=__name__):
    app = Flask(name)
    app.config.from_object(FlaskHistConfiguration)
    db.init_app(app)

    import app.portfolio.blueprint as blueprint
    app.register_blueprint(blueprint.portfolio, url_prefix='/display')
    return app

hist = create_app()
hist.app_context().push()