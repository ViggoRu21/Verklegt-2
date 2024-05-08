from django.db import models
from django.core.validators import RegexValidator
import datetime

from utilities_static.models import User, Company, Category, EmploymentType, Status
import datetime


# Create your models here.

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_ssn = models.CharField(max_length=10)

    class Meta:
        app_label = 'company'


class JobListing(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary_low = models.IntegerField()
    salary_high = models.IntegerField()
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE)

    class Meta:
        app_label = 'company'


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_applications')
    date = models.DateField(default=datetime.date.today)
    listing = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    models.UniqueConstraint(fields=['user', 'listing'], name='unique_application')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='company_applications')

    class Meta:
        app_label = 'company'
