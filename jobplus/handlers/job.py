from flask import Blueprint,flash,abort,redirect,url_for,render_template,request,current_app
from flask_login import login_required,current_user
from jobplus.models import User,db,Job,CompanyDetail,Delivery
from datetime import datetime

job = Blueprint('job',__name__,url_prefix='/job')

@job.route('/')
def index():
    job = Job.query.all()
    time_now = datetime.utcnow()

    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('/job/job.html',pagination=pagination,job=job,time=time_now)

@job.route('/<int:job_id>')
def job_details(job_id):
    time_now = datetime.utcnow()
    job = Job.query.filter_by(id = job_id).first()
    company = CompanyDetail.query.filter_by(id = job.company_id).first()
    return render_template('/job/job_details.html',job = job,company = company,time=time_now)

@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.resume_url is None:
        flash('你还没有上传简历哦', 'warning')
    elif job.current_user_is_applied:
        flash('已经投递过该职位', 'warning')
    else:
        d = Delivery(
            job_id=job.id,
            user_id=current_user.id,
            company_id=job.company.id
        )
        db.session.add(d)
        db.session.commit()
        flash('投递成功', 'success')
    return redirect(url_for('job.job_details', job_id=job.id))