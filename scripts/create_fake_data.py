import os
import sys
from random import randint
import random
import datetime

import django
from django_countries import countries
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
sys.path.append(".")

django.setup()
fake = Faker()

from company.models import Company, Recruiter, JobListing, Application, ApplicationEducation, ApplicationResume, \
    ApplicationRecommendations, ApplicationWorkExperience
from applicant.models import Applicant, Education, Resume, Experience, Recommendation
from utilities_static.models import Category, EmploymentType, Status
from django.contrib.auth.models import User
from script_constants import job_categories, employment_types, status_types, NUM_COMPANIES, NUM_LISTINGS_PER_COMPANY, \
    NUM_APPLICATIONS_PER_LISTING
from generate_files import generate_logo, generate_avatar, generate_pdf_resume

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# APPLICANTS

def create_fake_applicant() -> Applicant:
    try:
        user = User.objects.create_user(username=fake.user_name(), first_name=fake.first_name(),
                                        last_name=fake.last_name(), email=fake.email(), password="pw")
        country_list = list(countries)
        applicant = Applicant.objects.create(
            user=user,
            street_name=fake.street_name(),
            house_number=fake.building_number(),
            country=random.choice(country_list),
            city=fake.city(),
            postal_code=fake.postcode(),
            ssn=fake.ssn(),
            phone_number =  fake.bothify(text='+#########'),
            gender=fake.random_element(elements=('Male', 'Female', 'Non-binary')),
            completed_profile=True
        )
        applicant.applicant_image = str(generate_avatar(applicant))
        applicant.save()
        return applicant
    except Exception as e:
        print(f"Error creating applicant: {e}")


def create_fake_education(applicant: Applicant) -> None:
    for _ in range(fake.random_int(min=1, max=3)):
        Education.objects.create(
            applicant=applicant,
            school=fake.company(),
            level=fake.random_element(elements=("Bachelor's", "Master's", "PhD")),
            additional_info=fake.text(max_nb_chars=100),
            location=fake.city(),
            start_date=fake.date_between(start_date="-10y", end_date="-3y"),
            end_date=fake.date_between(start_date="-2y", end_date="today")
        )


def create_fake_resume(applicant: Applicant) -> None:
    for i in range(fake.random_int(min=1, max=3)):
        Resume.objects.create(
            applicant=applicant,
            resume=str(generate_pdf_resume(applicant, fake, i))
        )


def create_fake_experience(applicant: Applicant) -> None:
    for _ in range(fake.random_int(min=1, max=5)):
        Experience.objects.create(
            applicant=applicant,
            company_name=fake.company(),
            start_date=fake.date_between(start_date="-10y", end_date="-2y"),
            end_date=fake.date_between(start_date="-1y", end_date="today"),
            main_responsibility=fake.paragraph(nb_sentences=randint(3, 5))
        )


def create_fake_recommendation(applicant: Applicant) -> None:
    for _ in range(fake.random_int(min=1, max=3)):
        Recommendation.objects.create(
            applicant=applicant,
            name=fake.name(),
            phone_number=fake.bothify(text='+#########'),
            company_name=fake.company()
        )


# UTILITIES STATIC

def create_job_categories() -> None:
    for category in job_categories:
        Category.objects.get_or_create(field=category)


def create_employment_types() -> None:
    for type_name in employment_types:
        EmploymentType.objects.get_or_create(type=type_name)


def create_statuses() -> None:
    for status_type in status_types:
        Status.objects.get_or_create(type=status_type)


# COMPANIES

def create_fake_company() -> Company:
    name = fake.company()
    ssn = fake.bothify(text='######-####')
    phone_number = fake.bothify(text='+#########')
    info = f"<p> {fake.paragraph(nb_sentences=randint(3, 10))} <p/>"

    logo_path = generate_logo(name)

    return Company.objects.create(
        name=name,
        ssn=ssn,
        phone_number=phone_number,
        location=fake.city(),
        info=info,
        logo=logo_path
    )


def create_fake_recruiter(company: Company) -> Recruiter:
    user = User.objects.create_user(username=fake.user_name(), email=fake.email(), first_name=fake.first_name(),
                                    last_name=fake.last_name(), password="pw")
    return Recruiter.objects.create(user=user, company_ssn=company.ssn)


def create_fake_job_listing(company: Company, recruiter: Recruiter) -> JobListing:
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
        location=fake.city(),
        employment_type=employment_type,
        description=f"<p> {fake.paragraph(nb_sentences=randint(5, 10))} </p>"
    )


def create_fake_application(applicant: Applicant, job_listing: JobListing) -> Application:
    status = Status.objects.order_by('?').first()
    application = Application.objects.create(
        applicant=applicant,
        recruiter=job_listing.recruiter,
        listing=job_listing,
        status=status
    )
    return application


def create_related_application_data(application: Application) -> None:
    ApplicationEducation.objects.create(application=application, education=Education.objects.order_by('?').first())
    ApplicationRecommendations.objects.create(application=application,
                                              recommendation=Recommendation.objects.order_by('?').first())
    ApplicationWorkExperience.objects.create(application=application,
                                             work_experience=Experience.objects.order_by('?').first())
    ApplicationResume.objects.create(application=application, resume=Resume.objects.order_by('?').first())


# POPULATE

def populate(num_companies: int, num_listings: int, num_applications: int) -> None:
    num_applicants = fake.random_int(min=10, max=15)

    for _ in range(num_applicants):
        new_applicant = create_fake_applicant()
        create_fake_education(new_applicant)
        create_fake_experience(new_applicant)
        create_fake_resume(new_applicant)
        create_fake_recommendation(new_applicant)

    create_job_categories()
    create_employment_types()
    create_statuses()

    for _ in range(num_companies):
        company = create_fake_company()
        recruiter = create_fake_recruiter(company)
        for _ in range(num_listings):
            job_listing = create_fake_job_listing(company, recruiter)
            for _ in range(num_applications):
                applicant = Applicant.objects.order_by('?').first()
                application = create_fake_application(applicant, job_listing)
                create_related_application_data(application)


populate(NUM_COMPANIES, NUM_LISTINGS_PER_COMPANY, NUM_APPLICATIONS_PER_LISTING)
