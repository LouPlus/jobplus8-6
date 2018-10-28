from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError,TextAreaField,SelectField
from wtforms.validators import Length,Email,EqualTo,DataRequired
from jobplus.models import db,User,CompanyDetail,Job
from flask_wtf.file import FileField,FileRequired
import os

class UserRegisterForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(),Length(3,24)])
    email=StringField('邮箱',validators=[DataRequired(),Email()])
    password=PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    repeat_password=PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('提交')
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
            raise ValidationError('用户名已存在')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

class EditForm(FlaskForm):
    email=StringField('邮箱',validators=[DataRequired(),Email()])
    password=PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    realname=StringField('真实姓名',validators=[DataRequired(),Length(3,24)])
    phone=StringField('电话',validators=[DataRequired(),Length(3,11)])
    submit=SubmitField('提交')
    def update_user(self,user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user 
    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('email not exit')

class LoginForm(FlaskForm):
    email=StringField('邮箱',validators=[DataRequired(),Email()])
    password=PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    remember_me=BooleanField('记住我')
    submit=SubmitField('提交')
    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    def validate_password(self,field):
        user=User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class CompanyProfileForm(FlaskForm):
    username = StringField('企业名称')
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
        user.username = self.username.data
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
    name = StringField('真实姓名')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    phone = StringField('手机号码',validators=[DataRequired()])
    password = PasswordField('密码(不填写保持不变)')
    resume = FileField('upload resume',validators=[FileRequired()])
    submit = SubmitField('提交')

    def upload_resume(self):
        f = self.resume.data
        filename = self.real_name.data+'.pdf'
        f.save(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'static',
            'resumes',
            filename
            ))
        return filename

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
    experience=SelectField(
        'experience requirement',
        choices=[
        ('0','0'),('1','1'),('2','2'),('3','3'),
        ('1-3','1-3'),('3-5','3-5'),('5+','5+')])
    degree=SelectField(
        'degree requirement',
        choices=[('batcheler','batcheler'),('master','master'),('doctor','doctor')])
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























