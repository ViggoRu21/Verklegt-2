import os
import sys
from random import randint
import django
from faker import factory, Faker
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
sys.path.append(".")

django.setup()
fake = Faker()

from company.models import *
from applicant.models import *
from utilities_static.models import *
from django.contrib.auth.models import User
from script_constants import job_categories, employment_types, status_types, NUM_COMPANIES, NUM_LISTINGS_PER_COMPANY, \
    NUM_APPLICATIONS_PER_LISTING
from generate_images import generate_logo, generate_avatar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


## APPLICANTS

def create_fake_applicant() -> Applicant:
    try:
        user = User.objects.create_user(username=fake.user_name(), first_name=fake.first_name(),
                                        last_name=fake.last_name(), email=fake.email())
        print("DEFINED A USER")

        applicant = Applicant.objects.create(
            user=user,
            street_name=fake.street_name(),
            house_number=fake.building_number(),
            country=fake.country(),
            city=fake.city(),
            postal_code=fake.postcode(),
            ssn=fake.ssn(),
            phone_number=fake.msisdn(),
            gender=fake.random_element(elements=('Male', 'Female', 'Non-binary'))
        )
        print("HERE")
        applicant.applicant_image = str(generate_avatar(applicant))
        print("IIIMAGE" + str(applicant.applicant_image))
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
            additional_info=fake.text(max_nb_chars=200),
            location=fake.city(),
            start_date=fake.date_between(start_date="-10y", end_date="-3y"),
            end_date=fake.date_between(start_date="-2y", end_date="today")
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
            phone_number=fake.unique.msisdn()[-7:],
            company_name=fake.company()
        )


## UTILITIES STATIC


def create_job_categories():
    for category in job_categories:
        Category.objects.get_or_create(field=category)


def create_employment_types():
    for type_name in employment_types:
        EmploymentType.objects.get_or_create(type=type_name)


def create_statuses():
    for status_type in status_types:
        Status.objects.get_or_create(type=status_type)


## COMPANIES

def create_fake_company():
    # Generate basic company data
    name = fake.company()
    ssn = fake.bothify(text='##-###-####')
    phone_number = fake.unique.phone_number()
    formatted_phone_number = ''.join(filter(str.isdigit, phone_number))[:15]
    info = fake.paragraph(nb_sentences=randint(3, 10))

    # Generate a simple logo
    logo_path = generate_logo(name)

    # Create and return the Company object
    return Company.objects.create(
        name=name,
        ssn=ssn,
        phone_number=formatted_phone_number,
        location=fake.city(),
        info=info,
        logo=logo_path
    )


def create_fake_recruiter(company) -> Recruiter:
    user = User.objects.create_user(username=fake.user_name(), email=fake.email(), first_name=fake.first_name(),
                                    last_name=fake.last_name())
    recruiter_ssn = company.ssn
    return Recruiter.objects.create(user=user, company_ssn=company.ssn)


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
        location=fake.city(),
        employment_type=employment_type,
        description=fake.paragraph(nb_sentences=randint(5, 10))
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


def create_related_application_data(application) -> None:
    ApplicationEducation.objects.create(application=application, education=Education.objects.order_by('?').first())
    ApplicationRecommendations.objects.create(application=application,
                                              recommendation=Recommendation.objects.order_by('?').first())
    ApplicationWorkExperience.objects.create(application=application,
                                             work_experience=Experience.objects.order_by('?').first())


## POPULATE

def populate(num_companies: int, num_listings: int, num_applications: int) -> None:
    num_applicants = fake.random_int(min=10, max=15)

    for _ in range(num_applicants):
        new_applicant = create_fake_applicant()
        print("IMAGE" + str(new_applicant.applicant_image))
        create_fake_education(new_applicant)
        print("APPLICANT", new_applicant.user.first_name)
        create_fake_experience(new_applicant)
        # TODO resumes
        create_fake_recommendation(new_applicant)

    print("made fake applicants")

    create_job_categories()
    create_employment_types()
    create_statuses()

    print("made fake categories")

    for _ in range(num_companies):
        company = create_fake_company()
        print("Made fake company")
        recruiter = create_fake_recruiter(company)
        for _ in range(num_listings):
            job_listing = create_fake_job_listing(company, recruiter)
            print("Made fake job listing")
            for _ in range(num_applications):
                applicant = Applicant.objects.order_by('?').first()
                application = create_fake_application(applicant, recruiter, job_listing)
                create_related_application_data(application)


populate(NUM_COMPANIES, NUM_LISTINGS_PER_COMPANY, NUM_APPLICATIONS_PER_LISTING)
