from faker import Factory
from jobplus.models import db,Job,User,CompanyDetail
fake = Factory().create('zh_CN')

def iter_job():
    for i in range(10):
        yield Job(
        jobname=fake.job(),
        salary = fake.random_int(),
        exprience = fake.random_digit_or_empty(),
        location = fake.city(),
        job_description = fake.word(),
        job_requirement = fake.sentence()
        )

def iter_user():
    for i in range(10):
        yield User(
        username = fake.name(),
        email = fake.ascii_safe_email(),
        job = fake.job(),
        _password = fake.password()
        )

def iter_company():
    for i in range(10):
        yield CompanyDetail(
        logo = fake.url(),
        site = fake.url(),
        location = fake.address(),
        description = fake.word(),
        about = fake.word(),
        tags = fake.word(),
        stack = fake.word(),
        team_introduction = fake.word(),
        welfares = fake.word(),
        field = fake.word(),
        finance_stage = fake.word(),
        )

def run():
    for user in iter_user():
        db.session.add(user)

    for job in iter_job():
        db.session.add(job)

    for company in iter_company():
        db.session.add(company)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


