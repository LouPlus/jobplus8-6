from flask import Blueprint,flash,abort,redirect,url_for,render_template,request,current_app
from jobplus.forms import CompanyProfileForm,PublishForm
from flask_login import login_required,current_user
from jobplus.models import User,db,Job,CompanyDetail,Delivery
from jobplus.decorators import company_required

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/')
def index():
    page = request.args.get('page',1,type=int)
    pagination = User.query.filter(User.role == User.ROLE_COMPANY).order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=12,
        error_out = False
        )
    return render_template('company/company.html',pagination=pagination,active='company')
@company.route('/<int:company_id>')
def company_details(company_id):
    job = Job.query.filter_by(company_id = company_id)
    job_count = Job.query.filter_by(company_id = company_id).count()
    company = CompanyDetail.query.filter_by(id = company_id).first()
    return render_template('/company/company_details.html',company = company,job=job,job_count=job_count)


@company.route('/profile/',methods=['GET','POST'])
@login_required
def profile():
    # if not current_user.is_company:
    #     flash('您不是企业用户', 'warning')
    #     return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company)
    form.name.data = current_user.realname
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/companyprofile.html',form=form)


@company.route('/<int:company_id>/admin')
@company_required
def admin_index(company_id):
    company=User.query.get_or_404(company_id)
    page=request.args.get('page',default=1,type=int)
    pagination=Job.query.filter_by(company_id=company.company.id).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False)
    return render_template('company/admin_index.html',pagination=pagination,company_id=company_id)


@company.route('/<int:company_id>/admin/publish_job',methods=['GET','POST'])
@company_required
def publish_job(company_id):
    if current_user.id!=company_id:
        abort(404)
    form=PublishForm()
    if form.validate_on_submit():
        form.publish_job(current_user)
        flash('publish job success','success')
        return redirect(url_for('company.admin_index',company_id=current_user.id))
    return render_template('company/publish.html',form=form,company_id=company_id)

@company.route('/<int:id>')
@company_required
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
    return redirect(url_for('company.admin_index'))

@company.route('/<int:company_id>/admin/edit_job/<int:job_id>')
@company_required
def edit_job(company_id,job_id):
    if current_user.id != company_id:
        abort(404)
    job=Job.query.get_or_404(job_id)
    if job.company_id != current_user.company.id:
        abort(404)
    form=PublishForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('update job success','success')
        return redirect(url_for('company.admin_index',company_id=current_user.id))
    return render_template('company/edit_job.html',form=form,company_id=company_id,job=job)

@company.route('/<int:company_id>/admin/jobs/<int:job_id>/delete')
@company_required
def delete_job(company_id,job_id):
    if current_user.id != company_id:
        abort(404)
    job=Job.query.get_or_404(job_id)
    if job.company_id!=current_user.company.id:
        abort(404)
    db.session.delete(job)
    db.session.commit()
    flash('delete success','success')
    return redirect(url_for('company.admin_index',company_id=current_user.id))

@company.route('/<int:company_id>/admin/apply')
@company_required
def admin_apply(company_id):
    if not current_user.is_admin and not current_user.id==company_id:
        abort(404)
    status = request.args.get('status','all')
    page = request.args.get('page',default=1,type=int)
    q = Delivery.query.filter_by(company_id=company_id)
    if status=='waiting':
        q=q.filter(Delivery.status==Delivery.STATUS_WAITING)
    elif status=='accept':
        q=q.filter(Delivery.status==Delivery.STATUS_ACCEPT)
    elif status=='reject':
        q=q.filter(Delivery.status==Delivery.STATUS_REJECT)
    pagination = q.order_by(Delivery.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
        )
    return render_template('company/admin_apply.html',pagination=pagination,company_id=company_id)

@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/accept/')
@company_required
def admin_apply_accept(company_id,delivery_id):
    d = Delivery.query.get_or_404(delivery_id)
    if current_user.id != company_id:
        abort(404)
    d.status = Delivery.STATUS_ACCEPT
    flash('delivery accepted','success')
    db.session.add(d)
    db.session.commit()
    return redirect(url_for('company.admin_apply',company_id=company_id))

@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/reject/')
@company_required
def admin_apply_reject(company_id,delivery_id):
    d = Delivery.query.get_or_404(delivery_id)
    if current_user.id != company_id:
        abort(404)
    d.status = Delivery.STATUS_REJECT
    flash('delivery reject','success')
    db.session.add(d)
    db.session.commit()
    return redirect(url_for('company.admin_apply',company_id=company_id))

