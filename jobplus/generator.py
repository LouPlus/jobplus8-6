from faker import Factory
import random
from jobplus.models import db,Job,User,Company
import random
fake = Factory().create('zh_CN')

def iter_job():
    for i in range(50):
        yield Job(
        jobname=fake.job(),
        salary_min = random.randint(2,5) * 1000,
        salary_max = random.randint(6,10) * 1000,
        exprience = random.randint(0,5),
        location = fake.city(),
        job_tag = fake.word(),
        job_description = fake.word(),
        job_requirement = fake.sentence(),
        company_id = random.randint(1,15)
        )

def iter_user():
    for i in range(15):
        yield User(
        username = fake.name(),
        email = fake.ascii_safe_email(),
        job = fake.job(),
        _password = fake.password(),
        phone=fake.phone_number(),
        realname=fake.name(),
        role=random.choice([10,20])
        )

def iter_company():
    for i in range(15):
        yield Company(
        company_name = fake.company(),
        website = fake.url(),
        company_location = fake.address(),
        company_description = fake.text(),
        user_id=random.randint(1,15)
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


