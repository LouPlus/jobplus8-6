from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import Length,Email,EqualTo,DataRequired
from jobplus.models import db,User,CompanyDetail,Job

class UserRegisterForm(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(3,24)])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    repeat_password=PasswordField('repeatpassword',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Submit')
    def create_user(self):
    	user=User()
    	user.username=self.username.data
    	user.email=self.email.data
    	user.password=self.password.data
    	db.session.add(user)
    	db.session.commit()
    	return user
    def update_user(self,user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    def validate_username(self,field):
    	if User.query.filter_by(username=field.data).first():
    		raise ValidationError('User already exist')
    def validate_email(self,field):
    	if User.query.filter_by(email=field.data).first():
    		raise ValidationError('email already exist')

class EditForm(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    realname=StringField('realname',validators=[DataRequired(),Length(3,24)])
    phone=StringField('phone',validators=[DataRequired(),Length(3,11)])
    submit=SubmitField('Submit')
    def update_user(self,user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user 
    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('email not exit')

class LoginForm(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Submit')
    def validate_email(self,field):
    	if not User.query.filter_by(email=field.data).first():
    		raise ValidationError('email not register')
    def validate_password(self,field):
    	user=User.query.filter_by(email=self.email.data).first()
    	if user and not user.check_password(field.data):
    		raise ValidationError('Wrong password')

class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    password = PasswordField('密码(不填写保持不变)')
    slug = StringField('Slug', validators=[DataRequired(), Length(3, 24)])
    location = StringField('地址', validators=[Length(0, 64)])
    site = StringField('公司网站', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('一句话描述', validators=[Length(0, 100)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')

    def updated_profile(self,user):
        user.username = self.name.data
        user.email = self.email.data
        user.phone = self.phone.data
        if self.password.data:
            user.password = self.password.data

        if user.company:
            company_detail = user.company

        else:
            company_detail = CompanyDetail()
            company_detail.user_id = user.id
        self.populate_obj(company_detail)
        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()

class UserProfileForm(FlaskForm):
    name = StringField('名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    password = PasswordField('密码(不填写保持不变)')
    submit = SubmitField('提交')

    def updated_profile(self,user):
        user.realname = self.name.data
        user.email = self.email.data
        user.phone = self.phone.data
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()

class PublishForm(FlaskForm):
    jobname=StringField('jobname',validators=[DataRequired()])
    salary_min=StringField('min salary')
    salary_max=StringField('max salary')
    location=StringField('location')
    job_tag=StringField('job tag')
    job_description=StringField('job description')
    submit=SubmitField('Publish')
    def publish_job(self,company):
        job=Job()
        self.populate_obj(job)
        job.company_id=company.company.id
        db.session.add(job)
        db.session.commit()
        return job
    def update_job(self,job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job























