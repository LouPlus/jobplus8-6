from flask import Blueprint
from forms import CompanyConfigForm

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/admin/profile',methods=['get','POST'])
@login_required
def company_admin():
	form = CompanyConfigForm()