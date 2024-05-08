import utilities_static.models
from django.db import models
from django.core.validators import RegexValidator
from utilities_static.models import Category, EmploymentType, Status
from django.contrib.auth.models import User
import datetime
from applicant.models import Applicant, Education, Resume, Recommendation, Experience


# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_ssn = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=14, unique=True)
    company_info = models.TextField()

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return self.company_name


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_ssn = models.CharField(max_length=10)

    class Meta:
        app_label = 'company'

    def __str__(self) -> str:
        return f"Recruiter: {self.user.first_name} {str(self.user.last_name)}"


class JobListing(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_added = models.DateField(default=datetime.date.today)
    due_date = models.DateField(default="1990-01-01")
    job_title = models.CharField(max_length=100, default="None")
    salary_low = models.IntegerField()
    salary_high = models.IntegerField()
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'

    def __str__(self):
        return f"{self.company} - {self.job_title} - {self.due_date} - {self.salary_low} - {self.salary_high}"


class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    listing = models.OneToOneField(JobListing, on_delete=models.CASCADE)
    models.UniqueConstraint(fields=['user', 'listing'], name='unique_application')
    status = models.OneToOneField(Status, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'


class ApplicationEducation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'


class ApplicationResume(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'


class ApplicationRecommendations(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'


class ApplicationWorkExperience(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    work_experience = models.ForeignKey(Experience, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'
