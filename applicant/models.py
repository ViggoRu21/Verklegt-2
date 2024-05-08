from django.db import models
from django.core.validators import RegexValidator
import datetime
from utilities_static.models import User


# Create your models here.

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        app_label = 'applicant'


class Education(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    additional_info = models.TextField(max_length=300)
    location = models.CharField(max_length=100)

    class Meta:
        app_label = 'applicant'


class Resume(models.Model):
    #TODO figure out how to let them upload files
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    class Meta:
        app_label = 'applicant'


class Experience(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    main_responsibility = models.TextField(max_length=1000)

    class Meta:
        app_label = 'applicant'


class Recommendation(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=7, unique=True)
    company_name = models.CharField(max_length=100)

    class Meta:
        app_label = 'applicant'
