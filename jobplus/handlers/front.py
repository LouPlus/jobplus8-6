from jobplus.models import Job,Company,User
from flask import render_template,Blueprint,flash,request,current_app,redirect,url_for
from flask_login import login_user,logout_user,login_required
from datetime import datetime
from jobplus.forms import UserRegisterForm,LoginForm

front = Blueprint('front',__name__)

@front.route('/')
def index():

    job=Job.query.all()
    company = Company.query.all()
    time_now=datetime.utcnow()
    
    return render_template('index.html',job=job,company=company,time=time_now)

@front.route('/userregister',methods=['POST','GET'])
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
        flash('Login success','success')
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
    job = Job.query.all()
    time_now = datetime.utcnow()

    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('./job/job.html',pagination=pagination,job=job,time=time_now)

@front.route('/job/<int:job_id>')
def job_details(job_id):
    time_now = datetime.utcnow()
    job = Job.query.filter_by(id = job_id).first()
    company = Company.query.filter_by(id = job.company_id)
    return render_template('./job/job_details.html',job = job,company = company,time=time_now)


@front.route('/company/<int:company_id>')
def company_details(company_id):
    job = Job.query.filter_by(company_id = company_id)
    company = Company.query.filter_by(id = company_id).first()
    return render_template('/company/company_details.html',company = company,job=job)