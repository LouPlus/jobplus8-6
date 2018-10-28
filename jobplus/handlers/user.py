from flask import Blueprint,flash,redirect,url_for,render_template,request,current_app
from jobplus.forms import UserProfileForm
from flask_login import login_required,current_user
from jobplus.models import User,db,Job

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/profile',methods=['GET','POST'])
def profile():
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('user/userprofile.html',form=form)


@user.route('/user_detail')
@login_required
def user_detail():

    
    return render_template('user/user_detail.html')