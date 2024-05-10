import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
sys.path.append(".")
import django
django.setup()
from faker import factory, Faker
fake = Faker()
import datetime
from django.contrib.auth.models import User
from random import randint
from company.models import *
from applicant.models import *
from utilities_static.models import *


## APPLICANTS

def create_fake_applicant():
    user = User.objects.create_user(username=fake.user_name(), first_name=fake.first_name(), last_name=fake.last_name())
    applicant = Applicant.objects.create(user=user)
    return applicant


def create_fake_education(applicant):
    for _ in range(fake.random_int(min=1, max=3)):  # Each applicant might have 1 to 3 educations
        Education.objects.create(
            applicant=applicant,
            school=fake.company(),
            level=fake.random_element(elements=("Bachelor's", "Master's", "PhD")),
            additional_info=fake.text(max_nb_chars=200),
            location=fake.city(),
            start_date=fake.date_between(start_date="-10y", end_date="-3y"),
            end_date=fake.date_between(start_date="-2y", end_date="today")
        )


def create_fake_experience(applicant):
    for _ in range(fake.random_int(min=1, max=5)):  # Each applicant might have 1 to 5 jobs
        Experience.objects.create(
            applicant=applicant,
            company_name=fake.company(),
            start_date=fake.date_between(start_date="-10y", end_date="-2y"),
            end_date=fake.date_between(start_date="-1y", end_date="today"),
            main_responsibility=fake.paragraph(nb_sentences=3)
        )



def create_fake_recommendation(applicant):
    for _ in range(fake.random_int(min=1, max=3)):  # Each applicant might have 1 to 3 recommendations
        Recommendation.objects.create(
            applicant=applicant,
            name=fake.name(),
            phone_number=fake.unique.msisdn()[-7:],
            company_name=fake.company()
        )


## UTILITIES STATIC

job_categories = [
    "Accounting",
    "Administration",
    "Human Resources",
    "Information Technology",
    "Engineering",
    "Marketing",
    "Sales",
    "Customer Service",
    "Education",
    "Healthcare",
    "Construction",
    "Logistics",
    "Technology",
    "Creative Arts",
    "Legal",
    "Science and Research"
]


def create_job_categories():
    for category in job_categories:
        Category.objects.get_or_create(field=category)


def create_employment_types():
    types = ['Full Time', 'Part Time', 'Summer Job']
    for type_name in types:
        EmploymentType.objects.get_or_create(type=type_name)


def create_statuses():
    status_types = ['New', 'Maybe', 'Hired', 'Denied', 'Deleted', 'Interview']
    for status_type in status_types:
        Status.objects.get_or_create(type=status_type)


## COMPANIES

def create_fake_company():
    company_name = fake.company()
    company_ssn = fake.bothify(text='##-###-####')
    phone_number = fake.unique.phone_number()
    formatted_phone_number = ''.join(filter(str.isdigit, phone_number))[:15]
    company_info = fake.paragraph(nb_sentences=3)
    return Company.objects.create(
        company_name=company_name,
        company_ssn=company_ssn,
        phone_number=formatted_phone_number,
        company_info=company_info,
        company_logo='path/to/your/image.jpg'
    )


def create_fake_recruiter(company):
    user = User.objects.create_user(username=fake.user_name(), email=fake.email(), first_name=fake.first_name(),
                                    last_name=fake.last_name())
    recruiter_ssn = company.company_ssn
    return Recruiter.objects.create(user=user, company_ssn=recruiter_ssn)


def create_fake_recruiter(company):
    user = User.objects.create_user(username=fake.user_name(), email=fake.email(), first_name=fake.first_name(),
                                    last_name=fake.last_name())
    recruiter_ssn = company.company_ssn
    return Recruiter.objects.create(user=user, company_ssn=recruiter_ssn)


def create_fake_job_listing(company, recruiter):
    category = Category.objects.order_by('?').first()
    employment_type = EmploymentType.objects.order_by('?').first()
    return JobListing.objects.create(
        company=company,
        job_title=fake.job(),
        date_added=datetime.date.today(),
        due_date=fake.date_between(start_date="today", end_date="+1y"),
        salary_low=randint(30000, 50000),
        salary_high=randint(50001, 120000),
        recruiter=recruiter,
        category=category,
        employment_type=employment_type
    )


def create_fake_application(applicant, recruiter, job_listing):
    status = Status.objects.order_by('?').first()
    application = Application.objects.create(
        applicant=applicant,
        recruiter=recruiter,
        listing=job_listing,
        status=status
    )
    return application


def create_related_application_data(application):
    # Education, Resume, Recommendations, Work Experience
    ApplicationEducation.objects.create(application=application, education=Education.objects.order_by('?').first())
    # ApplicationResume.objects.create(application=application, resume=Resume.objects.order_by('?').first())
    ApplicationRecommendations.objects.create(application=application,
                                              recommendation=Recommendation.objects.order_by('?').first())
    ApplicationWorkExperience.objects.create(application=application,
                                             work_experience=Experience.objects.order_by('?').first())


## POPULATE
def populate():
    num_applicants = fake.random_int(min=10, max=15)

    for _ in range(num_applicants):
        new_applicant = create_fake_applicant()
        create_fake_education(new_applicant)
        create_fake_experience(new_applicant)
        # TODO resumes
        create_fake_recommendation(new_applicant)

    print("made fake applicants")

    create_job_categories()
    create_employment_types()
    create_statuses()

    print("made fake categories")

    num_companies = 5

    for _ in range(num_companies):
        company = create_fake_company()
        print("Made fake company")
        recruiter = create_fake_recruiter(company)
        for _ in range(10):
            job_listing = create_fake_job_listing(company, recruiter)
            print("Made fake job listing")
            for _ in range(5):
                applicant = Applicant.objects.order_by('?').first()
                application = create_fake_application(applicant, recruiter, job_listing)
                create_related_application_data(application)

populate()