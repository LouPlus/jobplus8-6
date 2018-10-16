from flask import Blueprint,flash,redirect,url_for,render_remplate
from forms import CompanyConfigForm

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/admin/profile',methods=['get','POST'])
@login_required
def company_admin():
	form = CompanyConfigForm()
	if form.validate_on_submit():
		form.create_company()
		flash('success create company','sucess')
		return redirect(url_for('company.detail'))
	return render_remplate('create_company.html',form=form)