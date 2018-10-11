from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_time=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    job = db.Column(db.String(64))
    def __repr__(self):
        return '<User: {}'.format(self.username)

    # @password.setter
    # def password(self, orig_password):
    #     self._password = generate_password_hash(orig_password)

    # def check_password(self, password):
    #     return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Job(Base):
    __tablename__ = 'job'
    id=db.Column(db.Integer,primary_key=True)
    jobname=db.Column(db.String(64),nullable=False)
    salary=db.Column(db.String(64))
    exprience=db.Column(db.String(64))
    location=db.Column(db.String(64))
    job_description=db.Column(db.String(256))
    job_requirement=db.Column(db.String(256))
    company_id=db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE'))
    

class Company(Base):
    __tablename__ = 'company'
    id=db.Column(db.Integer,primary_key=True)
    company_name=db.Column(db.String(128),index=True,unique=True,nullable=False)
    website=db.Column(db.String(128))
    company_location=db.Column(db.String(64))
    job=db.relationship('Job',backref='company',uselist=False)
    company_description=db.Column(db.String(256))
    
