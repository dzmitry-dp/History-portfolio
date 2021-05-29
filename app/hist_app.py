from app import create_app
from config import FlaskHistConfiguration

hist = create_app()
hist.config.from_object(FlaskHistConfiguration)
