from flask import Blueprint,render_template,request,current_app,redirect,url_for,flash
from jobplus.decorators import admin_required
from jobplus.models import User,Company,Job,db
from jobplus.forms import UserRegisterForm,EditForm

admin=Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/users')
@admin_required
def users():
	page=request.args.get('page',default=1,type=int)
	pagination=User.query.paginate(page=page,per_page=current_app.config['INDEX_PER_PAGE'],error_out=False)
	return render_template('admin/users.html',pagination=pagination)

@admin.route('/users/create',methods=['GET','POST'])
@admin_required
def create_user():
	form=UserRegisterForm()
	if form.validate_on_submit():
		form.create_user()
		flash('create user success','success')
		return redirect(url_for('admin.users'))
	return render_template('admin/create_user.html',form=form)

@admin.route('/users/<int:id>/edit',methods=['GET','POST'])
@admin_required
def edit_user(id):
	user=User.query.get_or_404(id)
	form=EditForm(obj=user)
	if form.validate_on_submit():
		form.update_user(user)
		flash('update user success','success')
	return render_template('admin/edit_user.html',user=user,form=form)

@admin.route('/users/<int:id>')
@admin_required
def allow_user(id):
	user=User.query.get_or_404(id)
	if user.allow==0:
		user.allow=1
		flash('%s is use'%user.username,'success')
	else:
		user.allow=0
		flash('%s is forbidden'%user.username,'success')
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('admin.users'))

@admin.route('/jobs')
@admin_required
def jobs():
	page=request.args.get('page',default=1,type=int)
	pagination=Job.query.paginate(page=page,per_page=current_app.config['INDEX_PER_PAGE'],error_out=False)
	return render_template('admin/jobs.html',pagination=pagination)

@admin.route('/jobs/<int:id>')
@admin_required
def online_job(id):
	job=Job.query.get_or_404(id)
	if job.online==0:
		job.online=1
		flash('%s online success'%job.jobname,'success')
	else:
		job.online=0
		flash('%s downline success'%job.jobname,'success')
	db.session.add(job)
	db.session.commit()
	return redirect(url_for('admin.jobs'))