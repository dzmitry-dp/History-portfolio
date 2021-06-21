class FlaskHistConfiguration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1@localhost/hist'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1@localhost/hist'
    UPLOAD_FOLDER = 'display/img'

positions_table = 'test'
history_table = 'm_test'