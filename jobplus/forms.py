from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Length,Email,EqualTo,DataRequired,URL

class UserRegisterForm(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(3,24)])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    repeat_password=PasswordField('repeatpassword',validators=[Required(),EqualTo('password')])
    submit=SubmitField('Submit')
    def create_user(self):
    	user=User()
    	user.username=self.username.data
    	user.email=self.email.data
    	user.password=self.password.data
    	db.session.add(user)
    	db.session.commit()
    	return user
    def validate_username(self,field):
    	if User.query.filter_by(username=field.data).first():
    		raise ValidationError('User already exist')
    def validate_email(self,field):
    	if User.query.filter_by(email=field.data).first():
    		raise ValidationError('email already exist')
class LoginForm(FlaskForm):
    email=EmailField('email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired(),Length(6,24)])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Submit')
    def validate_email(self,field):
    	if not User.query.filter_by(email=field.data).first():
    		raise ValidationError('email not register')
    def validate_password(self,field):
    	user=User.query.filter_by(email=self.email.data).first():
    	if user and not user.check_password(field.data):
    		raise ValidationError('Wrong password')

class CompanyConfigForm(FlaskForm):
    company_name = StringField('companyname',validators=[DataRequired(),Length(6,24)])
    email = EmailField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),Length(6,24)])
    address = StringField('address',validators=[DataRequired(),Length(6,36)])
    logo_url = StringField('logo_url',validators=[DataRequired(),URL()])
    company_url = StringField('company_url',validators=[DataRequired(),URL()])
    describe = StringField('describe',validators=[DataRequired(),Length(6,36)])
    description = StringField('description',validators=[DataRequired(),Length(6,128)])







