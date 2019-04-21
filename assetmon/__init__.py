import os

from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        #return 'Hello, World!'
        return app.instance_path
    from assetmon.routes import bp
    app.register_blueprint(bp)

    from assetmon.models import db
    #user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    #security = Security

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
