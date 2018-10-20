from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError
from wtforms.validators import Length,Email,EqualTo,DataRequired
from jobplus.models import db,User

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









