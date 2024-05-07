
# Create your models here.
from django.db import models as django_models

import company.models
import utilities_static.models
from utilities_static.models import User
from company.models import Application


# Create your models here.

class Applicant(django_models.Model):
    user = django_models.OneToOneField(User, on_delete=django_models.CASCADE, primary_key=True)

    class Meta:
        app_label = 'applicant'


class Education(django_models.Model):
    applicant = django_models.ForeignKey(Applicant, on_delete=django_models.CASCADE)
    school = django_models.CharField(max_length=100)
    level = django_models.CharField(max_length=100)
    additional_info = django_models.TextField(max_length=300)
    location = django_models.CharField(max_length=100)

    class Meta:
        app_label = 'applicant'


class Resume(django_models.Model):
    pass

    class Meta:
        app_label = 'applicant'


class Experience(django_models.Model):
    company_name = django_models.CharField(max_length=100)
    start_date = django_models.DateField()
    end_date = django_models.DateField()
    main_responsibility = django_models.TextField(max_length=1000)

    class Meta:
        app_label = 'applicant'


class Recommendation(django_models.Model):
    name = django_models.CharField(max_length=100)
    phone_number = django_models.CharField(max_length=7, unique=True)
    company_name = django_models.CharField(max_length=100)

    class Meta:
        app_label = 'applicant'


class ApplicationEducation(django_models.Model):
    application = django_models.ForeignKey(company.models.Application, on_delete=django_models.CASCADE)
    education = django_models.ForeignKey(Education, on_delete=django_models.CASCADE)


class ApplicationResume(django_models.Model):
    application = django_models.ForeignKey(company.models.Application, on_delete=django_models.CASCADE)
    resume = django_models.ForeignKey(Resume, on_delete=django_models.CASCADE)


class ApplicationRecommendations(django_models.Model):
    application = django_models.ForeignKey(company.models.Application, on_delete=django_models.CASCADE)
    recommendation = django_models.ForeignKey(Recommendation, on_delete=django_models.CASCADE)


class ApplicationWorkExperience(django_models.Model):
    application = django_models.ForeignKey(company.models.Application, on_delete=django_models.CASCADE)
    work_experience = django_models.ForeignKey(Experience, on_delete=django_models.CASCADE)
