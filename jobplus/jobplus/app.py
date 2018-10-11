from flask import Flask
from flask_migrate import Migrate
from jobplus.config import configs
from flask_login import LoginManager
from jobplus.models import db,User,Job,Company

def register_blueprint(app):
    from .handlers import front
    app.register_blueprint(front)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    register_blueprint(app)

    return app



