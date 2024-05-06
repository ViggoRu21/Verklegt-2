from django.db import models
#from django.core.validators import RegexValidator
import datetime


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    SSN = models.CharField(max_length=11,
                           unique=True)
    # TODO: validators=[RegexValidator(r'^\d{3}-\d{2}-\d{4}$', 'Enter a valid SSN.')])
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, unique=True)
    authentication_hash = models.CharField(max_length=256, unique=True)
    # TODO validate


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_ssn = models.CharField(max_length=10)


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_ssn = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=14, unique=True)
    company_info = models.TextField()


class JobListings(models.Model):
    id = models.AutoField(primary_key=True)


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    listing = models.OneToOneField(JobListings, on_delete=models.CASCADE)
    models.UniqueConstraint(fields=['user', 'listing'], name='unique_application')


class Education(models.Model):
    school = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    additional_info = models.TextField(max_length=300)
    location = models.CharField(max_length=100)


class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    main_responsibility = models.TextField(max_length=1000)


class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=7, unique=True)
    company_name = models.CharField(max_length=100)