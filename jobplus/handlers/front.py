from jobplus.models import Job,Company
from flask import render_template,Blueprint,flash,request,current_app
from flask_login import login_user,logout_user,login_required
from datetime import datetime

front = Blueprint('front',__name__)

@front.route('/')
def index():

    job=Job.query.all()
    company = Company.query.all()
    time_now=datetime.utcnow()
    
    return render_template('index.html',job=job,company=company,time=time_now)

@front.route('/userregister')
def userregister():
    form=UserRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('Register success,Please Login','success')
        return redirect(url_for('front.login'))
    return render_template('userregister.html',form=form)

@front.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        return redirect(url_for('front.index'))
    return render_template('login.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout','success')
    return redirect(url_for('front.index'))

@front.route('/job')
def job():
    job=Job.query.all()
    time_now=datetime.utcnow()

    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('./job/job.html',pagination=pagination,job=job,time=time_now)

