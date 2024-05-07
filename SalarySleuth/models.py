from django.db import models
from django.core.validators import RegexValidator
import datetime


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    SSN = models.CharField(max_length=11, unique=True,
                           validators=[RegexValidator(r'^\d{3}-\d{2}-\d{4}$', 'Enter a valid SSN.')])
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, unique=True)
    authentication_hash = models.CharField(max_length=256, unique=True)  #, validators=['TODO: Add password rules'])

    class Meta:
        app_label = 'SalarySleuth'


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        app_label = 'SalarySleuth'


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_ssn = models.CharField(max_length=10)

    class Meta:
        app_label = 'SalarySleuth'


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_ssn = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=14, unique=True)
    company_info = models.TextField()

    class Meta:
        app_label = 'SalarySleuth'


class Category(models.Model):
    field = models.CharField(max_length=100)


class EmploymentType(models.Model):
    type = models.CharField(max_length=100)


class JobListing(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary_low = models.IntegerField()
    salary_high = models.IntegerField()
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)

    class Meta:
        app_label = 'SalarySleuth'


class Status(models.Model):
    type = models.CharField(max_length=100)


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    listing = models.OneToOneField(JobListing, on_delete=models.CASCADE)
    models.UniqueConstraint(fields=['user', 'listing'], name='unique_application')
    status = models.OneToOneField(Status, on_delete=models.CASCADE)

    class Meta:
        app_label = 'SalarySleuth'


class Education(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    additional_info = models.TextField(max_length=300)
    location = models.CharField(max_length=100)

    class Meta:
        app_label = 'SalarySleuth'


class Resume(models.Model):
    pass

    class Meta:
        app_label = 'SalarySleuth'


class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    main_responsibility = models.TextField(max_length=1000)

    class Meta:
        app_label = 'SalarySleuth'


class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=7, unique=True)
    company_name = models.CharField(max_length=100)

    class Meta:
        app_label = 'SalarySleuth'


class ApplicationEducation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)


class ApplicationResume(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)


class ApplicationReccomendations(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)


class ApplicationWorkExperience(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    work_experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
