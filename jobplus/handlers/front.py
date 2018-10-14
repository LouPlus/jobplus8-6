from jobplus.models import Job,Company
from flask import render_template,Blueprint,flash
from flask_login import login_user,logout_user,login_required

front = Blueprint('front',__name__)

@front.route('/')
def index():

    job=Job.query.all()
    company = Company.query.all()
    
    return render_template('index.html',job=job,company=company)

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
