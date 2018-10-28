from jobplus.models import Job,CompanyDetail,User,db
from flask import render_template,Blueprint,flash,request,current_app,redirect,url_for
from flask_login import login_user,logout_user,login_required
from datetime import datetime
from jobplus.forms import UserRegisterForm,LoginForm

front = Blueprint('front',__name__)

@front.route('/')
def index():

    job=Job.query.all()
    company = CompanyDetail.query.all()
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

@front.route('/companyregister',methods=['GET','POST'])
def companyregister():
    form=UserRegisterForm()
    if form.validate_on_submit():
        u=form.create_user()
        u.role=User.ROLE_COMPANY
        db.session.add(u)
        db.session.commit()      
        flash('Register success,Please Login','success')
        return redirect(url_for('front.login'))
    return render_template('companyregister.html',form=form)

@front.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.allow==1:
            login_user(user,form.remember_me.data)
            flash('Login success','success')
            if user.is_company:
                return redirect(url_for('company.profile'))
            if user.is_admin:
                return redirect(url_for('front.index'))
            else:
                return redirect(url_for('user.profile'))
        else:
            flash('this user is forbidden','warning')
    return render_template('login.html',form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout','success')
    return redirect(url_for('front.index'))






