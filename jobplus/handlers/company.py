from flask import Blueprint,flash,redirect,url_for,render_template,request,current_app
from jobplus.forms import CompanyProfileForm,PublishForm
from flask_login import login_required,current_user
from jobplus.models import User,db,Job,CompanyDetail
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
    form = CompanyProfileForm(obj=current_user.company_detail)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)




@company.route('/<int:company_id>/admin')
@company_required
def admin_index(company_id):
    company=User.query.get_or_404(company_id)
    page=request.args.get('page',default=1,type=int)
    pagination=Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False)
    return render_template('company/index.html',pagination=pagination,company_id=company_id,company=company)

@company.route('/<int:company_id>/admin/publish_job',methods=['GET','POST'])
@company_required
def publish_job(company_id):
    form=PublishForm()
    if form.validate_on_submit():
        form.publish_job()
        flash('publish job success','success')
        return redirect(url_for('company.index',company_id=company_id))
    return render_template('company/publish.html',form=form,company_id=company_id)
