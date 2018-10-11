from jobplus.models import Job
from flask import render_template,Blueprint

front = Blueprint('front',__name__)

@front.route('/')
def index():
    jobs=Job.query.all()
    
    return render_template('index.html',job=jobs[0])