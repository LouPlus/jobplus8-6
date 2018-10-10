from flask import Flask,render_template
from flask_migrate import Migrate
from jobplus.config import configs
from jobplus.models import db,User,Job,Company
from flask_login import LoginManager

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)

    @app.route('/')
    def index():
        jobs=Job.query.all()
        
        return render_template('index.html',job=jobs[0])
    return app


